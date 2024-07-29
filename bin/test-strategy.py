#!/usr/bin/env python3
# coding: utf8
import argparse
import os

from xfund import daos
from xfund import setups
from xfund import strategies
from xfund.core import decimals
from xfund.strategies.regular import RegularInvest


def parse_args():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument('--out', default='out/', help='outdir')

    group = parser.add_argument_group('basic')
    group.add_argument('--code', required=True, help='fund code')
    group.add_argument('--start', help='start date')
    group.add_argument('--end', help='end date')
    group.add_argument('--init', default=0, type=float, help='amount to init position')
    group.add_argument('--interval', default='w1',
                       help='regular interval: w<weekday> for weekly or d<k> for every k days')
    group.add_argument('--delta', default=1_000, type=float, help='delta amount of regular')
    group.add_argument('--decrease', help='decrease config of regular amount: `<rate_grid>:<decrease_amount>`')
    group.add_argument('--strategy', default=[], nargs='*', help='strategy conf, like `name:arg1,arg2`')

    return parser, parser.parse_args()


def main():
    parser, args = parse_args()

    sql = setups.setup_sql()
    fund = daos.FundDao(sql).get_fund(args.code)
    if fund is None:
        parser.error('no fund found, check --code')
    navs = daos.NavDao(sql).list_navs(args.code, start=args.start, end=args.end)
    if len(navs) == 0:
        parser.error('no nav found, check --start/--end or list-nav first')
    os.makedirs(args.out, exist_ok=True)
    outname = os.path.join(args.out, f'{fund.code}.{fund.name}')

    strategy_list = []
    for s in args.strategy:
        s = strategies.parse_strategy(s)
        strategy_list.append(s)

    invest = RegularInvest(init_amount=args.init,
                           interval=args.interval,
                           delta_amount=args.delta,
                           decrease=args.decrease,
                           strategies=strategy_list,
                           )
    record = invest.backtest(navs)
    beg, end = navs[0], navs[-1]
    value_rate = decimals.rate(end.value / beg.value - 1)
    print(f'> {fund.name}[{fund.code}]: {beg.date}~{end.date}, {value_rate:.2%}')
    print(f'* 持仓收益: {record.position_amount} - {record.position_cost} = {record.position_profit}'
          f', {record.position_profit_rate:.2%}')
    print(f'* 历史收益: {record.total_amount} - {record.total_cost} = {record.total_profit}'
          f', {record.total_profit_rate:.2%}')

    position_csv = f'{outname}.position.csv'
    record.write_positions(position_csv)
    buy_csv = f'{outname}.buy.csv'
    record.acc_buy.write_history(buy_csv)
    sell_csv = f'{outname}.sell.csv'
    record.acc_sell.write_history(sell_csv)
    record.print_total()

    print('* files:')
    tformat = '. {:<10} : {:<}'
    for name, csv_file in [
        ('position', position_csv),
        ('buy', buy_csv),
        ('sell', sell_csv),
    ]:
        print(tformat.format(name, csv_file))


if __name__ == '__main__':
    setups.setup_logging()
    main()
