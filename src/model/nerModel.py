import numpy as np
import os
import tensorflow as tf

from .utils.utils import minibatches, padSequences, getChunks
from .utils.logger import Progbar, printLog

class NERModel():
    def __init__(self, config):
        self.config = config
        self.sess   = None
        self.saver  = None
        self.idxToTag = {idx: tag for tag, idx in self.config.dictTags.items()}
    
    def reinitializeWeights(self, scopeName):
        variables = tf.contrib.framework.get_variables(scopeName)
        init = tf.variables_initializer(variables)
        self.sess.run(init)

    def addTrainOp(self, lrMethod, lr, loss, clip=-1):
        """
        lrMethod: (string) sgd method, for example "adam"
        lr: (tf.placeholder) tf.float32, learning rate
        loss: (tensor) tf.float32 loss to minimize
        clip: (python float) clipping of gradient. If < 0, no clipping
        """
        _lr_m = lrMethod.lower()
        with tf.variable_scope("train_step"):
            if _lr_m == 'adam': # sgd method
                optimizer = tf.train.AdamOptimizer(lr)
            elif _lr_m == 'adagrad':
                optimizer = tf.train.AdagradOptimizer(lr)
            elif _lr_m == 'sgd':
                optimizer = tf.train.GradientDescentOptimizer(lr)
            elif _lr_m == 'rmsprop':
                optimizer = tf.train.RMSPropOptimizer(lr)
            else:
                raise NotImplementedError("Unknown method {}".format(_lr_m))

            if clip > 0: # gradient clipping if clip is positive
                grads, vs     = zip(*optimizer.compute_gradients(loss))
                grads, gnorm  = tf.clip_by_global_norm(grads, clip)
                self.trainOp = optimizer.apply_gradients(zip(grads, vs))
            else:
                self.trainOp = optimizer.minimize(loss)


    def initializeSession(self):
        self.sess = tf.Session()
        self.sess.run(tf.global_variables_initializer())
        self.saver = tf.train.Saver()

    # reloade weights
    def reloadSession(self, dirModel):
        printLog("Reloading the latest model.")
        self.saver.restore(self.sess, dirModel)

    # save weights
    def saveSession(self):
        if not os.path.exists(self.config.dirModel):
            os.makedirs(self.config.dirModel)
        self.saver.save(self.sess, self.config.dirModel)

    def closeSession(self):
        self.sess.close()

    # save tf graph
    def addSummary(self):
        self.merged = tf.summary.merge_all()
        self.fileWriter = tf.summary.FileWriter(self.config.dirOutput, self.sess.graph)

    def train(self, train, dev):
        """
        train: dataset that yields tuple of (sentences, tags)
        dev: dataset
        """
        bestScore = 0
        nepochNoImprove = 0 # for early stopping
        self.addSummary() # save graph

        for epoch in range(self.config.nepochs):
            printLog("Epoch {:} out of {:}".format(epoch + 1, self.config.nepochs))

            score = self.runEpoch(train, dev, epoch)
            self.config.lr *= self.config.lrDecay # decay learning rate

            # early stopping and saving best parameters
            if score >= bestScore:
                nepochNoImprv = 0
                self.saveSession()
                bestScore = score
                printLog("- new best score!")
            else:
                nepochNoImprove += 1
                if nepochNoImprv >= self.config.nepochNoImprove:
                    printLog("- early stopping {} epochs without "\
                            "improvement".format(nepochNoImprv))
                    break

    def evaluate(self, test):
        """
        test: instance of class Dataset
        """
        metrics = self.runEvaluate(test)
        msg = " - ".join(["{} {:04.2f}".format(k, v)
                for k, v in metrics.items()])
        printLog(msg)

    def addPlaceholders(self):
        # shape = (batch size, max length of sentence in batch)
        self.wordIds = tf.placeholder(tf.int32, shape=[None, None],
                        name="wordIds")

        # shape = (batch size)
        self.sequenceLengths = tf.placeholder(tf.int32, shape=[None],
                        name="sequenceLengths")

        # shape = (batch size, max length of sentence, max length of word)
        self.charIds = tf.placeholder(tf.int32, shape=[None, None, None],
                        name="charIds")

        # shape = (batchSize, maxLength of sentence)
        self.wordLengths = tf.placeholder(tf.int32, shape=[None, None],
                        name="wordLengths")

        # shape = (batch size, max length of sentence in batch)
        self.labels = tf.placeholder(tf.int32, shape=[None, None],
                        name="labels")

        # hyper parameters
        self.dropout = tf.placeholder(dtype=tf.float32, shape=[],
                        name="dropout")
        self.lr = tf.placeholder(dtype=tf.float32, shape=[],
                        name="lr")


    def getFeedDict(self, words, labels=None, lr=None, dropout=None):
        if self.config.useChars:
            charIds, wordIds = zip(*words)
            wordIds, sequenceLengths = padSequences(wordIds, 0)
            charIds, wordLengths = padSequences(charIds, padtok=0, nlevels=2)
        else:
            wordIds, sequenceLengths = padSequences(words, 0)

        feed = {
            self.wordIds: wordIds,
            self.sequenceLengths: sequenceLengths
        }

        if self.config.useChars:
            feed[self.charIds] = charIds
            feed[self.wordLengths] = wordLengths

        if labels is not None:
            labels, _ = padSequences(labels, 0)
            feed[self.labels] = labels

        if lr is not None:
            feed[self.lr] = lr

        if dropout is not None:
            feed[self.dropout] = dropout

        return feed, sequenceLengths


    def addWordEmbeddingsOp(self):
        """
        If self.config.embeddings is not None and is a np array initialized
        with pre-trained word vectors, the word embeddings is just a look-up
        and we don't train the vectors. Otherwise, a random matrix with
        the correct shape is initialized.
        """
        with tf.variable_scope("words"):
            if self.config.embeddings is None:
                printLog("WARNING: randomly initializing word vectors")
                _wordEmbeddings = tf.get_variable(
                        name="_wordEmbeddings",
                        dtype=tf.float32,
                        shape=[self.config.nwords, self.config.dimWord])
            else:
                _wordEmbeddings = tf.Variable(
                        self.config.embeddings,
                        name="_wordEmbeddings",
                        dtype=tf.float32,
                        trainable=self.config.trainEmbeddings)

            wordEmbeddings = tf.nn.embedding_lookup(_wordEmbeddings, self.wordIds, name="wordEmbeddings")

        with tf.variable_scope("chars"):
            if self.config.useChars:
                # get char embeddings matrix
                _charEmbeddings = tf.get_variable(
                        name="_charEmbeddings",
                        dtype=tf.float32,
                        shape=[self.config.nchars, self.config.dimChar])
                charEmbeddings = tf.nn.embedding_lookup(_charEmbeddings,
                        self.charIds, name="charEmbeddings")

                # put the time dimension on axis=1
                s = tf.shape(charEmbeddings)
                charEmbeddings = tf.reshape(charEmbeddings,
                        shape=[s[0]*s[1], s[-2], self.config.dimChar])
                wordLengths = tf.reshape(self.wordLengths, shape=[s[0]*s[1]])

                # bi lstm on chars
                cellFw = tf.contrib.rnn.LSTMCell(self.config.hiddenSizeChar,
                        state_is_tuple=True)
                cellBw = tf.contrib.rnn.LSTMCell(self.config.hiddenSizeChar,
                        state_is_tuple=True)
                _output = tf.nn.bidirectional_dynamic_rnn(
                        cellFw, cellBw, charEmbeddings,
                        sequence_length=wordLengths, dtype=tf.float32)

                # read and concat output
                _, ((_, outputFw), (_, outputBw)) = _output
                output = tf.concat([outputFw, outputBw], axis=-1)

                # shape = (batch size, max sentence length, char hidden size)
                output = tf.reshape(output,
                        shape=[s[0], s[1], 2*self.config.hiddenSizeChar])
                wordEmbeddings = tf.concat([wordEmbeddings, output], axis=-1)
        self.wordEmbeddings =  tf.nn.dropout(wordEmbeddings, self.dropout)


    def addLogitsOp(self):
        """
        For each word in each sentence of the batch, it corresponds to a vector
        of scores, of dimension equal to the number of tags.
        """
        with tf.variable_scope("bi-lstm"):
            cellFw = tf.contrib.rnn.LSTMCell(self.config.hiddenSizeLstm)
            cellBw = tf.contrib.rnn.LSTMCell(self.config.hiddenSizeLstm)
            (outputFw, outputBw), _ = tf.nn.bidirectional_dynamic_rnn(
                    cellFw, cellBw, self.wordEmbeddings,
                    sequence_length=self.sequenceLengths, dtype=tf.float32)
            output = tf.concat([outputFw, outputBw], axis=-1)
            output = tf.nn.dropout(output, self.dropout)

        with tf.variable_scope("proj"):
            W = tf.get_variable("W", dtype=tf.float32,
                    shape=[2*self.config.hiddenSizeLstm, self.config.ntags])

            b = tf.get_variable("b", shape=[self.config.ntags],
                    dtype=tf.float32, initializer=tf.zeros_initializer())

            nsteps = tf.shape(output)[1]
            output = tf.reshape(output, [-1, 2*self.config.hiddenSizeLstm])
            pred = tf.matmul(output, W) + b
            self.logits = tf.reshape(pred, [-1, nsteps, self.config.ntags])

    def addPredOp(self):
        if not self.config.useCrf:
            self.labelsPred = tf.cast(tf.argmax(self.logits, axis=-1),
                    tf.int32)

    def addLossOp(self):
        if self.config.useCrf:
            logLikelihood, transParams = tf.contrib.crf.crf_log_likelihood(
                    self.logits, self.labels, self.sequenceLengths)
            self.transParams = transParams # need to evaluate it for decoding
            self.loss = tf.reduce_mean(-logLikelihood)
        else:
            losses = tf.nn.sparse_softmax_cross_entropy_with_logits(
                    logits=self.logits, labels=self.labels)
            mask = tf.sequence_mask(self.sequenceLengths)
            losses = tf.boolean_mask(losses, mask)
            self.loss = tf.reduce_mean(losses)
        tf.summary.scalar("loss", self.loss)

    def build(self):
        self.addPlaceholders()
        self.addWordEmbeddingsOp()
        self.addLogitsOp()
        self.addPredOp()
        self.addLossOp()

        self.addTrainOp(self.config.lrMethod, self.lr, self.loss,
                self.config.clip)
        self.initializeSession()

    def predictBatch(self, words):
        """
        words: list of sentences
        return labelsPred: list of labels for each sentence
        reurn sequence length
        """
        fd, sequenceLengths = self.getFeedDict(words, dropout=1.0)

        if self.config.useCrf:
            viterbiSequences = []
            logits, transParams = self.sess.run(
                    [self.logits, self.transParams], feed_dict=fd)

            # iterate over the sentences because no batching in vitervi_decode
            for logit, sequenceLength in zip(logits, sequenceLengths):
                logit = logit[:sequenceLength]
                viterbiSeq, viterbiScore = tf.contrib.crf.viterbi_decode(
                        logit, transParams)
                viterbiSequences += [viterbiSeq]

            return viterbiSequences, sequenceLengths

        else:
            labelsPred = self.sess.run(self.labelsPred, feed_dict=fd)

            return labelsPred, sequenceLengths

    def runEpoch(self, train, dev, epoch):
        """
        train: dataset that yields tuple of sentences, tags
        dev: dataset
        epoch: (int) index of the current epoch
        return f1: (python float), score to select model on, higher is better
        """
        # for progress bar
        batchSize = self.config.batchSize
        nbatches = (len(train) + batchSize - 1) // batchSize
        prog = Progbar(target=nbatches)

        # iterate over dataset
        for i, (words, labels) in enumerate(minibatches(train, batchSize)):
            fd, _ = self.getFeedDict(words, labels, self.config.lr,
                    self.config.dropout)

            _, trainLoss, summary = self.sess.run(
                    [self.trainOp, self.loss, self.merged], feed_dict=fd)

            prog.update(i + 1, [("train loss", trainLoss)])
            # save
            if i % 10 == 0:
                self.fileWriter.add_summary(summary, epoch*nbatches + i)

        metrics = self.runEvaluate(dev)
        msg = " - ".join(["{} {:04.2f}".format(k, v)
                for k, v in metrics.items()])
        printLog(msg)
        return metrics["f1"]

    def runEvaluate(self, test):
        """
        test: dataset that yields tuple of (sentences, tags)
        return metrics: (dict) metrics["acc"] = 98.4, ...
        """
        accs = []
        correctPreds, totalCorrect, totalPreds = 0., 0., 0.
        for words, labels in minibatches(test, self.config.batchSize):
            labelsPred, sequenceLengths = self.predictBatch(words)

            for lab, labPred, length in zip(labels, labelsPred,
                                             sequenceLengths):
                lab      = lab[:length]
                labPred = labPred[:length]
                accs    += [a == b for (a, b) in zip(lab, labPred)]

                labChunks      = set(getChunks(lab, self.config.dictTags))
                labPredChunks = set(getChunks(labPred, self.config.dictTags))

                correctPreds += len(labChunks & labPredChunks)
                totalPreds   += len(labPredChunks)
                totalCorrect += len(labChunks)

        p   = correctPreds / totalPreds if correctPreds > 0 else 0
        r   = correctPreds / totalCorrect if correctPreds > 0 else 0
        f1  = 2 * p * r / (p + r) if correctPreds > 0 else 0
        acc = np.mean(accs)
        return {"acc": 100*acc, "f1": 100*f1, "Pred": p, "Recall": r}

    def predict(self, wordsRaw):
        words = [self.config.processingWord(w) for w in wordsRaw]
        #print(words)
        if type(words[0]) == tuple:
            words = zip(*words)


        predIds, _ = self.predictBatch([words])
        preds = [self.idxToTag[idx] for idx in list(predIds[0])]
        return preds
