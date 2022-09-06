# coding: utf8
import typing

import numpy as np

EQUITY_DECIMALS = 3  # 份额小数位
VALUE_DECIMALS = 4  # 净值小数位
AMOUNT_DECIMALS = 2  # 金额小数位
RATE_DECIMALS = 4  # 收益率小数位


# 持仓资产、收益及成本价说明：https://www.futuhk.com/hans/support/topic448?lang=zh-cn


class AccDelta:
    def __init__(self, date, amount, equity):
        self.date = date
        self.amount = amount
        self.equity = equity


class Accumulation:
    def __init__(self):
        self.amount = 0
        self.equity = 0
        self.histories: typing.List[AccDelta] = []

    def append(self, date, amount, equity):
        self.amount = np.around(self.amount + amount, AMOUNT_DECIMALS)
        self.equity = np.around(self.equity + equity, EQUITY_DECIMALS)
        self.histories.append(AccDelta(date=date,
                                       amount=amount,
                                       equity=equity,
                                       ))

    @property
    def average_cost(self):
        if self.equity == 0:
            cost = 0.0
        else:
            cost = self.amount / self.equity
        return np.around(cost, VALUE_DECIMALS)

    def write_history(self, out_csv):
        with open(out_csv, 'w') as outf:
            outf.write(','.join(['date', 'amount', 'equity']) + '\n')
            for item in self.histories:
                outf.write(f'{item.date},{item.amount},{item.equity}\n')
            outf.write(f'total,{self.amount},{self.equity}\n')


class PositionSnap:
    def __init__(self, date, net_value, equity, diluted_cost):
        self.date = date
        self.net_value = net_value
        self.equity = equity
        # 持仓金额
        self.amount = np.around(equity * net_value, AMOUNT_DECIMALS)
        if diluted_cost == 0:
            diluted_cost = net_value
        # 持仓收益
        self.profit = np.around((net_value - diluted_cost) * equity)
        # 持仓收益率
        self.profit_rate = np.around((net_value - diluted_cost) / diluted_cost, RATE_DECIMALS)

    @property
    def average_cost(self):
        if self.equity == 0:
            cost = 0.0
        else:
            cost = self.amount / self.equity
        return np.around(cost, VALUE_DECIMALS)


class ProfitRecord:
    def __init__(self):
        # 累计买入
        self.acc_buy = Accumulation()
        # 累计卖出
        self.acc_sell = Accumulation()
        # 收益率曲线
        self.position_histories: typing.List[PositionSnap] = []
        self.position_equity = 0

    @property
    def diluted_cost(self):
        """摊薄成本价"""
        if self.position_equity == 0:
            cost = 0
        else:
            cost = (self.acc_buy.amount - self.acc_sell.amount) / self.position_equity
        return np.around(cost, VALUE_DECIMALS)

    def settle(self, date, net_value):
        """当天结算收益"""
        snap = PositionSnap(date, net_value, self.position_equity, self.diluted_cost)
        self.position_histories.append(snap)

    def buy(self, date, net_value, amount):
        """买入"""
        amount = np.around(amount, AMOUNT_DECIMALS)
        equity = np.around(amount / net_value, decimals=EQUITY_DECIMALS)
        self.acc_buy.append(date, amount, equity)
        self.position_equity = np.around(self.position_equity + equity, EQUITY_DECIMALS)

    def sell(self, date, net_value, position):
        """赎回"""
        equity = np.around(self.position_equity * position, decimals=EQUITY_DECIMALS)
        amount = np.around(equity * net_value, AMOUNT_DECIMALS)
        self.acc_sell.append(date, amount, equity)
        self.position_equity = np.around(self.position_equity - equity, EQUITY_DECIMALS)

    def write_positions(self, out_csv):
        with open(out_csv, 'w') as outf:
            outf.write(','.join(['date', 'equity', 'amount', 'profit', 'rate']) + '\n')
            for snap in self.position_histories:
                outf.write(','.join([
                    snap.date,
                    str(snap.equity),
                    str(snap.amount),
                    str(snap.profit),
                    '{:.2%}'.format(snap.profit_rate),
                ]) + '\n')

    def write_total(self, out_csv):
        with open(out_csv, 'w') as outf:
            outf.write(','.join(['', 'equity', 'amount', 'avg_cost']))
            outf.write(f'buy,{self.acc_buy.equity},{self.acc_buy.amount},{self.acc_buy.average_cost}\n')
            outf.write(f'sell,{self.acc_sell.equity},{self.acc_sell.amount},{self.acc_sell.average_cost}\n')
            position = self.position_histories[-1]
            outf.write(f'position,{position.equity},{position.amount},{position.average_cost}\n')
            total_amount = np.around(self.acc_buy.amount + position.amount - self.acc_sell.amount, AMOUNT_DECIMALS)
            total_equity = np.around(self.acc_buy.equity + position.equity - self.acc_sell.equity, EQUITY_DECIMALS)
            total_avg = np.around(total_amount / total_equity, VALUE_DECIMALS)
            outf.write(f'total,{total_equity},{total_amount},{total_avg}\n')
