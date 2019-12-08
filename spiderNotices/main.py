"""

"""
import os
import sys;sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from scrapy import cmdline


def run_notices():
    cmdline.execute("scrapy crawl notices".split())


if __name__ == '__main__':
    run_notices()