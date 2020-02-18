"""
实时运行的脚本。
"""
import schedule
import datetime
import time
import os
import sys;sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from scrapy import cmdline


def run_notices():
    cmd_str = "scrapy crawl notices -a PAGE_SIZE=50"  # 带上外部参数
    print(datetime.datetime.now(), 'cmd运行{}'.format(cmd_str))
    cmdline.execute(cmd_str.split())


if __name__ == '__main__':
    schedule.every(3).hour.do(run_notices)
    while True:
        schedule.run_pending()
        time.sleep(1)

    # while True:
    #     try:
    #         run_notices()
    #     except Exception as e:
    #         print('执行异常{}'.format(e))
    #         time.sleep(60)
    #     else:
    #         print('正常结束')
    #         time.sleep(60 * 60)
