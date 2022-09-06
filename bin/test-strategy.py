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

    group = parser.add_argument_group('wave strategy')
    group.add_argument('--init', default=10_000, type=float, help='amount to init position')
    group.add_argument('--day', default=1, type=int, help='regular days')
    group.add_argument('--regular', default=1_000, type=float, help='regular amount')
    group.add_argument('--take_rate', default=0.1, type=float, help='rate to take profit')
    group.add_argument('--take_position', default=0.5, type=float, help='position when taking profit')
    group.add_argument('--add_rate', default=-0.1, type=float, help='rate to add position')
    group.add_argument('--add_amount', default=10_000, type=float, help='amount when adding position')

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
        init_amount=args.init,
        regular_days=args.day,
        regular_amount=args.regular,
        take_profit_rate=args.take_rate,
        take_profit_position=args.take_position,
        add_position_rate=args.add_rate,
        add_position_amount=args.add_amount,
    )
    record = strategy.backtest(navs)
    print(record.profit)

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
