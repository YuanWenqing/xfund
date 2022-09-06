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

    group = parser.add_argument_group('basic')
    group.add_argument('--code', help='fund code')
    group.add_argument('--start', help='start date')
    group.add_argument('--end', help='end date')
    group.add_argument('--init', default=10_000, type=float, help='amount to init position')
    group.add_argument('--day', default=1, type=int, help='regular days')
    group.add_argument('--regular', default=1_000, type=float, help='regular amount')

    group = parser.add_argument_group('add position')
    group.add_argument('--add_rate', default=-0.02, type=float, help='rate to add position')
    group.add_argument('--add_amount', default=10_000, type=float, help='amount when adding position')

    subs = parser.add_subparsers(title='strategy', dest='strategy')

    take_profit = subs.add_parser('take_profit')
    take_profit.add_argument('--take_rate', default=0.05, type=float, help='rate to take profit')
    take_profit.add_argument('--take_position', default=0.2, type=float, help='position when taking profit')

    drawback = subs.add_parser('drawback')
    drawback.add_argument('--back_day', default=5, type=int, help='rate to take profit')
    drawback.add_argument('--back_rate', default=0.05, type=float, help='rate to take profit')
    drawback.add_argument('--back_position', default=0.2, type=float, help='position when taking profit')

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

    if args.strategy == 'take_profit':
        strategy = strategies.TakeProfitStrategy(
            init_amount=args.init,
            regular_days=args.day,
            regular_amount=args.regular,
            add_position_rate=args.add_rate,
            add_position_amount=args.add_amount,

            take_profit_rate=args.take_rate,
            take_profit_position=args.take_position,
        )
    elif args.strategy == 'drawback':
        strategy = strategies.DrawbackStrategy(
            init_amount=args.init,
            regular_days=args.day,
            regular_amount=args.regular,
            add_position_rate=args.add_rate,
            add_position_amount=args.add_amount,

            drawback_days=args.back_day,
            drawback_rate=args.back_rate,
            drawback_position=args.back_position,
        )
    else:
        raise ValueError
    record = strategy.backtest(navs)
    print(record.profit)

    os.makedirs(args.out, exist_ok=True)
    outname = os.path.join(args.out, args.strategy)

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
