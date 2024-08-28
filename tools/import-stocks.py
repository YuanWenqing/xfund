#!/usr/bin/env python3
# coding: utf8
import argparse
import logging
import time

from xfund import biz
from xfund import inits


def parse_args():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        description='导入更新所有股票列表',
    )

    args = parser.parse_args()
    return args


def main():
    args = parse_args()
    ctx = biz.ServingContext()
    manager = ctx.stock_context.stock_manager

    beg = time.time()
    stocks = manager.import_all_stocks()
    timecost = time.time() - beg
    logging.info(f'timecost={timecost:.3f}s, num={len(stocks)}')


if __name__ == '__main__':
    inits.setup_logging()
    main()
