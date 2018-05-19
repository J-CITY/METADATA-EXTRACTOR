import os, sys
parentPath = os.path.abspath("..")
if parentPath not in sys.path:
	sys.path.insert(0, parentPath)

from model.utils.utils import CoNLLDataset
from model.nerModel import NERModel
from config.config import Config


def main():
    config = Config()
    model = NERModel(config)
    model.build()
    # model.restoreSession("results/crf/model.weights/") # optional, restore weights
    # model.reinitializeWeights("proj")

    dev   = CoNLLDataset(config.filenameDev, config.processingWord,
                         config.processingTag, config.maxIter)
    train = CoNLLDataset(config.filenameTrain, config.processingWord,
                         config.processingTag, config.maxIter)
    model.train(train, dev)

if __name__ == "__main__":
    main()
