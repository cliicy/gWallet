import time
import datetime
from datetime import datetime


def time_stamp(ts):
    tts = float(ts/1000)
    ta = time.localtime(tts)
    ots = time.strftime("%Y-%m-%d %H:%M:%S", ta)
    # print(ots)
    return ots


def num_transfer(num):
    """
    Volume换算成亿万单位
    :param num:
    :return:
    """
    vol = num
    sdd = num.replace(',', '')
    sdd = sdd.replace('¥ ', '')
    # print(sdd)
    yi_dd = float(sdd) * 0.00000001
    wan_dd = float(sdd) * 0.0001
    if yi_dd > 1:
        vol = '{0}{1}'.format(round(yi_dd, 1), '亿')
    elif wan_dd > 1:
        vol = '{0}{1}'.format(round(wan_dd, 1), '万')
    else:
        pass
    return vol


def timestamp_to_timestamp10(time_stamp):
    time_stamp = int(time_stamp * (10 ** (10 - len(str(time_stamp)))))
    return time_stamp


def timestamp_to_datetime_m(time_stamp):
    time_stamp = int(time_stamp * (10 ** (10 - len(str(time_stamp)))))
    time_local = time.localtime(time_stamp)
    tm = time.strftime("%Y-%m-%d %H:%M", time_local)
    return tm


def time_to_timestamp(time):
    stamp = int(time.mktime(time.timetuple())) * 1000
    return stamp


def strtime_to_today_timestamp(st):
    today = datetime.date.today().strftime("%Y/%m/%d ")
    st = today + st
    _time = datetime.datetime.strptime(st, "%Y/%m/%d %H:%M:%S")
    t = _time.timetuple()
    ts = int(time.mktime(t))*1000
    return ts
