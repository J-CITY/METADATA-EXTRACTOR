import os, sys
parentPath = os.path.abspath("../")
if parentPath not in sys.path:
	sys.path.insert(0, parentPath)

import os
import tensorflow as tf
from model.utils.logger import printLog

class BaseModel(object):
    def __init__(self, config):
        self.config = config
        self.sess   = None
        self.saver  = None

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
