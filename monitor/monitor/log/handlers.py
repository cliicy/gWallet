import logging
import os
import datetime
import pickle
from logging.handlers import RotatingFileHandler, SocketHandler


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


class Logger(object):
    """
    自定义log类
    """
    def __init__(self, logger, module_name='vwallet'):
        """

        :param logger:
        :param module_name:
        """
        # create a logger
        self.logger = logging.getLogger(logger)
        self.logger.setLevel(logging.DEBUG)
        self.module_name = module_name
        # create a name for logger
        log_path = os.path.abspath(os.path.join(os.getcwd(), '..\..\..', 'logs'))
        log_full_name = os.path.join(log_path, '%s%s' % (module_name, '.log'))
        # create a handler, which will be used to write log to file
        fh = VwalletHandler(log_full_name, when='D', backupCount=100)
        fh.setLevel(logging.DEBUG)

        # create one more handler, use it to write log info to console
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)

        # define the format of how handler output
        formatter = logging.Formatter('%(asctime)s - %(filename)s.%(funcName)s[%(lineno)d] '
                                      '- %(levelname)s - %(message)s')
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)
        # socket
        sh = VwalletSocketHandler('localhost', logging.handlers.DEFAULT_HTTP_LOGGING_PORT)
        sh.setLevel(logging.INFO)
        sh.setFormatter(formatter)
        # add handler to logger
        self.logger.addHandler(fh)
        self.logger.addHandler(ch)
        self.logger.addHandler(sh)

    def getlog(self):
        return self.logger


if __name__ == '__main__':
    ss = os.path.join('logs', '%s.%s' % ('aa.log', '%Y-%m-%d'))
    logger = Logger(__name__).getlog()
    logger.info('vw_test')

