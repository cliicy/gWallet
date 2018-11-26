from apscheduler.schedulers.background import BlockingScheduler

scheduler = BlockingScheduler()


@scheduler.scheduled_job('cron', minute='*/1', id='monitor_task', )
def syn_data():
    # 数据扫描
    pass


def do_set():
    s = set(['A', 'B', 'C'])
    print('A' in s)
    s = set([('Adam', 96),('Lisa', 85), ('Bart', 59)])
    for x in s:
        print(x[0], ':', x[1])
    s = set([1, 2, 3])
    s.add(4)
    print(s)
    s.add(3)
    print(s)
    months = set(['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec', ])
    x1 = 'Feb'
    x2 = 'Sun'
    if x1 in months:
        print('x1: ok')
    else:
        print('x1: error')
    if x2 in months:
        print('x2: ok')
    else:
        print('x2: error')


def do_list():
    a = range(4)
    print(a)
    print(a[::2])
    a[::2] = [0, -1]


if __name__ == '__main__':
    # 日志监听
    # scheduler.start()
    # do_set()
    do_list()
    pass
