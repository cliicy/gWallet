from apscheduler.schedulers.background import BlockingScheduler

scheduler = BlockingScheduler()


@scheduler.scheduled_job('cron', minute='*/1', id='monitor_task', )
def syn_data():
    # 数据扫描
    pass


if __name__ == '__main__':
    # 日志监听
    scheduler.start()
