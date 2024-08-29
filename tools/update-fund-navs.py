#!/usr/bin/env python3
# coding: utf8
import argparse
import logging
import time

from xfund import biz
from xfund.utils import logutil
from xfund.primary import dynamics


def parse_args():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        description='更新基金净值',
    )

    parser.add_argument('--code', nargs='+', required=True, help='code of fund')

    args = parser.parse_args()
    return args


def main():
    args = parse_args()
    ctx = biz.ServingContext()
    manager = ctx.fund_context.fund_manager

    beg = time.time()
    counts = dynamics.init_counts()
    for i in args.code:
        navs = manager.update_fund_navs(i)
        counts[i] = len(navs)
    timecost = time.time() - beg
    logging.info(f'timecost={timecost:.3f}s, counts={counts}')


if __name__ == '__main__':
    logutil.setup_logging()
    main()
