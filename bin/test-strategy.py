#!/usr/bin/env python3
# coding: utf8
import argparse

from fundstrategy import daos
from fundstrategy import setups
from fundstrategy import strategies


def parse_args():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument('--code', help='fund code')
    parser.add_argument('--start', help='start date')
    parser.add_argument('--end', help='end date')

    return parser.parse_args()


def main():
    args = parse_args()

    sql = setups.setup_sql()
    nav_dao = daos.NavDao(sql)
    navs = nav_dao.list_navs(args.code)
    navs.sort(key=lambda i: i.date)
    if args.start:
        navs = [i for i in navs if i.date >= args.start]
    if args.end:
        navs = [i for i in navs if i.date <= args.end]

    strategy = strategies.WaveRegularStrategy(
        init_amount=10_000,
        regular_days=2,
        regular_amount=1_000,
        take_profit_rate=0.05,
        take_profit_position=0.5,
        add_position_rate=-0.1,
        add_position_amount=10_000,
    )
    record = strategy.backtest(navs[100:110])
    record.print_profits()
    record.print_final()


if __name__ == '__main__':
    setups.setup_logging()
    main()
