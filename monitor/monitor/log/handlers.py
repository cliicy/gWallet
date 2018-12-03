import logging
import os
import datetime
import pickle
from logging.handlers import SocketHandler


class VwalletHandler(logging.FileHandler):
    def __init__(self, filename, when="D", backupCount=0, encoding=None,
                 delay=False):
        self.prefix = filename
        self.when = when.upper()
        # S - Every second a new file
        # M - Every minute a new file
        # H - Every hour a new file
        # D - Every day a new file
        if self.when == 'S':
            self.suffix = '%Y-$m-%d_%H-%M_%S'
            self.extMatch = r"^\d{4}-\d{2}-\d{2}_\d{2}-\d{2}-\d{2}$"
        elif self.when == 'M':
            self.suffix = '%Y-%m-%d_%H-%M'
            self.extMatch = r"^\d{4}-\d{2}-\d{2}_\d{2}-\d{2}"
        elif self.when == 'H':
            self.suffix = '%Y-%m-%d_%H'
            self.extMatch = r"^\d{4}-\d{2}-\d{2}_\d{2}"
        elif self.when == 'D':
            self.suffix = '%Y-%m-%d'
            self.extMatch = r"^\d{4}-\d{2}-\d{2}"
        else:
            raise ValueError("Invalid rollover interval specified: %s" % self.when)
        self.filefmt = os.path.join('%s.%s' % (self.prefix, self.suffix))
        self.filePath = datetime.datetime.now().strftime(self.filefmt)
        _dir = os.path.dirname(self.filePath)
        try:
            if os.path.exists(_dir) is False:
                os.makedirs(_dir)
        except Exception as e:
            print(e)
        logging.FileHandler.__init__(self,self.filePath, 'a', encoding, delay)


class VwalletSocketHandler(SocketHandler):
    """
    重写SocketHandler.makePickle
    """
    def makePickle(self, record):
        return pickle.dumps(record)


if __name__ == '__main__':
   pass
