"""
实时运行的脚本。
"""
import time
import os
import sys;sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from scrapy import cmdline


def run_notices():
    cmd_str = "scrapy crawl notices -a PAGE_SIZE=50"
    print('开始运行命令{}'.format(cmd_str))
    cmdline.execute(cmd_str.split())


if __name__ == '__main__':
    while True:
        try:
            run_notices()
        except Exception as e:
            print('执行异常{}'.format(e))
            time.sleep(60)
        else:
            print('正常结束')
            time.sleep(60 * 60)
