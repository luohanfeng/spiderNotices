"""

"""
import os
import sys;sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from scrapy import cmdline


def run_notices():
    cmd_str = "scrapy crawl notices"
    print('开始运行命令{}'.format(cmd_str))
    cmdline.execute(cmd_str.split())


if __name__ == '__main__':
    run_notices()