#!/usr/bin/env python3
# coding: utf8
import argparse
import os

from fundstrategy import daos
from fundstrategy import setups
from fundstrategy import strategies


def parse_args():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument('--out', default='out/', help='outdir')
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
    record = strategy.backtest(navs)

    os.makedirs(args.out, exist_ok=True)
    outname = os.path.join(args.out, 'strategy')

    position_csv = f'{outname}.position.csv'
    record.write_positions(position_csv)
    buy_csv = f'{outname}.buy.csv'
    record.acc_buy.write_history(buy_csv)
    sell_csv = f'{outname}.sell.csv'
    record.acc_sell.write_history(sell_csv)
    total_csv = f'{outname}.total.csv'
    record.write_total(total_csv)

    tformat = '{:<10} : {:<}'
    for name, csv_file in [
        ('position', position_csv),
        ('buy', buy_csv),
        ('sell', sell_csv),
        ('total', total_csv)
    ]:
        print(tformat.format(name, csv_file))


if __name__ == '__main__':
    setups.setup_logging()
    main()
