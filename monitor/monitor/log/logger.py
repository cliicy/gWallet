import logging
import os
import time
from monitor.monitor.log.handlers import VwalletHandler, VwalletSocketHandler


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
    # ss = os.path.join('logs', '%s.%s' % ('aa.log', '%Y-%m-%d'))
    # logger = Logger(__name__).getlog()
    # logger.info('vw_test')
    pass
    localtime = time.localtime(time.time())
    print('本地时间为1：', localtime)

    localtime = time.asctime(time.localtime(time.time()))
    print('本地时间为2：', localtime)

    print('Time 1', time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    print('Time 2', time.strftime("%a %b %d %H:%M:%S", time.localtime()))

    # a = "Sat Mar 28 22:24:24 2016"
    # print('Time 3', time.mktime(time.strptime(a, "%a %b %d %H:%M:%S %Y")))

    a = "Sat Mar 28 22:24:24 2016"
    print('Time 4', time.mktime(time.strptime(a, "%a %b %d %H:%M:%S %Y")))
    # ss = 'aaa,'
    # ss = ss.rstrip(',') + ';'
    # print(ss)
