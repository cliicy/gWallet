#  -*- coding:utf-8 -*-
# import urllib
# import urllib.parse
# import urllib.request
import requests
from app.config.secure import MonitoringAlarmConfig
from monitor.monitor.log.logger import Logger
import itchat
from email.mime.text import MIMEText
from email.header import Header
from email.utils import parseaddr, formataddr
import smtplib

logger = Logger(__name__, "vw_trades").getlog()


class HttpCommunicator:
    """
    http通信器
    """

    def http_get(self, url, params, headers):

        """
         http通信器get请求方法

        :param url: 请求接口地址 字符串类型 例如：'https://api.huobi.pro/market/history/kline'
        :param params: 请求参数  字典类型  例如：{'symbol': 'btcusdt', 'period': '1min', 'size': 150}
        :param headers: 请求头信息  字典类型 例如：{'Content-type': 'application/x-www-form-urlencoded',
                                                'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36'}
        :return: 返回json格式数据
        """
        headers = headers
        postdata = params
        logger.info("%s,%s,%s" % (url, params, headers))
        response = requests.get(url, postdata, headers=headers, timeout=5)
        try:

            if response.status_code == 200:
                logger.info("response:%s" % (response.json()))
                return response.json()
            else:
                logger.info("response:%s" % response.status_code)
                return
        except Exception as e:
            logger.error(e)
            return

    def http_post(self, url, params, headers, content_type=None, timeout=10):

        """
        http通信器post请求方法

        :param url: 请求接口地址 字符串类型 例如：'https://api.huobi.pro/market/history/kline'
        :param params: 请求参数  字典类型  例如：{'symbol': 'btcusdt', 'period': '1min', 'size': 150}
        :param headers: 请求头信息  字典类型 例如：{'Content-type': 'application/x-www-form-urlencoded',
                                                'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36'}
        :return: 返回json格式数据
        """

        headers = headers
        postdata = params
        if content_type is not None:
            logger.info("url:%s,postdata:%s,timeout:%s" % (url, postdata, timeout))
            response = requests.post(url, None, postdata, headers=headers, timeout=timeout)
        else:
            logger.info("url:%s,postdata:%s,timeout:%s" % (url, postdata, timeout))
            response = requests.post(url, postdata, headers=headers, timeout=timeout)
        try:
            if response.status_code == 200:
                logger.info("response:%s" % (response.json()))
                return response.json()
            else:
                return
        except Exception as e:
            logger.error(e)
            return


class SocketCommunicator:
    """
    socket通信器
    """
    # TODO 待开发


class WechartCommunicator(object):
    """
    微信信息发送类
    """

    def __init__(self):
        itchat.auto_login(hotReload=True)
        # itchat.run()

    @staticmethod
    def send(msg):
        """
        发送消息
        :param msg:
        :return:
        """
        itchat.auto_login(hotReload=True, enableCmdQR=-2)
        # a = itchat.search_chatrooms(name='研究院--知识图谱研究部')
        # f1 = itchat.search_friends(name='bingo')
        # 获取分别对应相应键值的用户

        for friend in MonitoringAlarmConfig.WECHART_FRIENDS:
            _f = itchat.search_friends(name=friend)
            logger.info(f"send wechart msg:{msg} to:{_f[0]['UserName']}")
            itchat.send_msg(msg, toUserName=_f[0]['UserName'])

        for rooms in MonitoringAlarmConfig.WECHART_CHATROOMS:
            _r = itchat.search_chatrooms(name=rooms)
            logger.info(f"send wechart msg:{msg} to:{_r[0]['UserName']}")
            itchat.send_msg(msg, toUserName=_r[0]['UserName'])


class EmailCommunicator(object):
    """
    电子邮件发送类
    """

    @staticmethod
    # 用来格式化邮件地址
    def _format_addr(s):
        name, addr = parseaddr(s)  # 这个函数会解析出姓名和邮箱地址
        return formataddr(( \
            Header(name, 'utf-8').encode(), \
            addr.encode('utf-8') if isinstance(addr, bytes) else addr))

    @staticmethod
    # 用来格式化邮件地址
    def _format_addr(s):
        name, addr = parseaddr(s)  # 这个函数会解析出姓名和邮箱地址
        return formataddr(( \
            Header(name, 'utf-8').encode(), \
            addr.encode('utf-8') if isinstance(addr, bytes) else addr))

    @staticmethod
    def send_mail(mail_text):
        from_addr = MonitoringAlarmConfig.EMAIL_FROM_ADDR
        password = MonitoringAlarmConfig.EMAIL_PASSWORD
        smtp_server = MonitoringAlarmConfig.EMAIL_SMTP_SERVER
        contact = MonitoringAlarmConfig.EMAIL_CONTACT
        msg = MIMEText(mail_text, 'plain', 'utf-8')
        # 设置发件人，收件人姓名和邮件主题
        msg['From'] = EmailCommunicator._format_addr(u'服务器<%s>' % from_addr)
        to_addr = ",".join(str(i) for i in contact)
        msg['To'] = EmailCommunicator._format_addr(u'负责人 <%s>' % to_addr)
        msg['Subject'] = Header(u'服务器程序告警邮件', 'utf-8').encode()

        server = smtplib.SMTP(smtp_server, 25)  # SMTP协议默认端口是25
        server.set_debuglevel(1)  # 打印出和SMTP服务器交互的所有信息
        server.login(from_addr, password)  # 登录服务器
        # 发送邮件，这里第二个参数是个列表，可以有多个收件人
        # 邮件正文是一个str，as_string()把MIMEText对象变成str
        logger.info(f"send msg:{mail_text} to:{str(contact)}")
        server.sendmail(from_addr, contact, msg.as_string())
        server.quit()


if __name__ == '__main__':
    # print(",".join(str(i) for i in MonitoringAlarmConfig.EMAIL_CONTACT))
    EmailCommunicator.send_mail("aaa")
