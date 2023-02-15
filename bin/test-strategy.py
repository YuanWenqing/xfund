#!/usr/bin/env python3
# coding: utf8
import argparse
import os

from fundstrategy import daos
from fundstrategy import setups
from fundstrategy import strategies
from fundstrategy.core.regular import RegularInvest


def parse_args():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument('--out', default='out/', help='outdir')

    group = parser.add_argument_group('basic')
    group.add_argument('--code', required=True, help='fund code')
    group.add_argument('--start', help='start date')
    group.add_argument('--end', help='end date')
    group.add_argument('--init', default=10_000, type=float, help='amount to init position')
    group.add_argument('--interval', default=1, type=int, help='interval days of regular')
    group.add_argument('--delta', default=1_000, type=float, help='delta amount of regular')

    group.add_argument('--strategy', default=[], nargs='*', help='strategy conf, like `name:arg1,arg2`')

    return parser, parser.parse_args()


def main():
    parser, args = parse_args()

    sql = setups.setup_sql()
    nav_dao = daos.NavDao(sql)
    navs = nav_dao.list_navs(args.code, start=args.start, end=args.end)
    if len(navs) == 0:
        parser.error('no nav found, check --start/--end or list-nav first')
    os.makedirs(args.out, exist_ok=True)
    outname = os.path.join(args.out, args.code)

    strategy_list = []
    for s in args.strategy:
        s = strategies.parse_strategy(s)
        strategy_list.append(s)

    invest = RegularInvest(init_amount=args.init,
                           interval_days=args.interval,
                           delta_amount=args.delta,
                           strategies=strategy_list,
                           )
    record = invest.backtest(navs)
    print(f'持仓收益: {record.position_amount} - {record.position_cost} = {record.position_profit}'
          f', {record.position_profit_rate:.2%}')
    print(f'历史收益: {record.total_amount} - {record.total_cost} = {record.total_profit}'
          f', {record.total_profit_rate:.2%}')

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
