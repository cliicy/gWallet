import time


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


