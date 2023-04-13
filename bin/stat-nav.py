#!/usr/bin/env python3
# coding: utf8
import argparse
import logging
import os.path

import matplotlib.pyplot as plt
import numpy as np

from fundstrategy import daos
from fundstrategy import setups
from fundstrategy.core import decimals


def parse_args():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument('code', help='fund code')
    parser.add_argument('--start', help='start date')
    parser.add_argument('--end', help='end date')
    parser.add_argument('--out', default='out/', help='outdir')
    parser.add_argument('--show', action='store_true', help='auto show?')

    return parser, parser.parse_args()


def main():
    def figure_increase_hist():
        increases = np.array([i.increase for i in navs])
        i_min = np.floor(np.min(increases))
        i_max = np.ceil(np.max(increases))
        bins = np.arange(i_min, i_max + 1, 0.5)

        plt.title(f'{fund.name}[{fund.code}]')
        # 汉字字体，优先使用楷体，找不到则使用黑体
        plt.rcParams['font.sans-serif'] = ['SimHei']
        # 正常显示负号
        plt.rcParams['axes.unicode_minus'] = False
        plt.hist(increases, bins=bins)

        outfile = os.path.join(args.out, f'{fund.code}.{fund.name}.png')
        plt.savefig(outfile)
        logging.info(f'image: {outfile}')

        if args.show:
            plt.show()

    def avg_weekday_value():
        avg_values = np.full(5, fill_value=np.inf)
        for d in range(1, 6):
            values = [i.value for i in navs if i.weekday == d]
            if len(values) > 0:
                avg_values[d - 1] = decimals.value(float(np.mean(values)))
        min_idx = np.argmin(avg_values)
        deltas = np.asarray([decimals.rate(i / avg_values[min_idx] - 1) for i in avg_values], dtype=float)
        tformat = '{:>10} | {:>10} | {:>10}'
        logging.info(tformat.format('weekday', 'avg_value', 'delta'))
        logging.info('-' * 40)
        for i, (value, delta) in enumerate(zip(avg_values, deltas)):
            if i == min_idx:
                weekday = f'*  {i + 1}'
            else:
                weekday = i + 1
            logging.info(tformat.format(weekday, value, f'{delta:.2%}'))

    parser, args = parse_args()
    sql = setups.setup_sql()
    fund = daos.FundDao(sql).get_fund(args.code)
    if fund is None:
        parser.error('no fund found, check --code')
    navs = daos.NavDao(sql).list_navs(args.code, start=args.start, end=args.end)
    if len(navs) == 0:
        parser.error('no nav found, check --start/--end or list-nav first')
    beg, end = navs[0], navs[-1]
    logging.info(f'{fund.name}[{fund.code}]: {beg.date} ~ {end.date}, {len(navs)} items')

    avg_weekday_value()
    figure_increase_hist()


if __name__ == '__main__':
    setups.setup_logging()
    main()
