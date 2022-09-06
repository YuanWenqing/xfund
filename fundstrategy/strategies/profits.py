# coding: utf8
import typing

import numpy as np

EQUITY_DECIMALS = 3  # 份额小数位
VALUE_DECIMALS = 4  # 净值小数位
AMOUNT_DECIMALS = 2  # 金额小数位
RATE_DECIMALS = 4  # 收益率小数位


def _around(value, decimals):
    return float(np.around(value, decimals))


# 持仓资产、收益及成本价说明：https://www.futuhk.com/hans/support/topic448?lang=zh-cn


class AccDelta:
    def __init__(self, date, amount, equity):
        self.date = date
        self.amount = amount
        self.equity = equity

    def __repr__(self):
        return f'<{self.__class__.__name__}: {self.date}, amount={self.amount:.2f}, equity={self.equity:.3f}>'


class Accumulation:
    def __init__(self, amount=0., equity: float = 0.):
        self.amount = amount
        self.equity = equity
        self.histories: typing.List[AccDelta] = []

    def __add__(self, other):
        res = Accumulation()
        res.amount = _around(self.amount + other.amount, AMOUNT_DECIMALS)
        res.equity = _around(self.equity + other.equity, EQUITY_DECIMALS)
        return res

    def __sub__(self, other):
        res = Accumulation()
        res.amount = _around(self.amount - other.amount, AMOUNT_DECIMALS)
        res.equity = _around(self.equity - other.equity, EQUITY_DECIMALS)
        return res

    def append(self, date, amount, equity):
        self.amount = _around(self.amount + amount, AMOUNT_DECIMALS)
        self.equity = _around(self.equity + equity, EQUITY_DECIMALS)
        delta = AccDelta(date=date,
                         amount=amount,
                         equity=equity,
                         )
        self.histories.append(delta)
        return delta

    @property
    def average_cost(self):
        if self.equity == 0:
            cost = 0.0
        else:
            cost = self.amount / self.equity
        return _around(cost, VALUE_DECIMALS)

    def write_history(self, out_csv):
        with open(out_csv, 'w') as outf:
            outf.write('date,amount,equity\n')
            tformat = '{:},{:.%df},{:.%df}\n' % (AMOUNT_DECIMALS, EQUITY_DECIMALS)
            for item in self.histories:
                outf.write(tformat.format(item.date, item.amount, item.equity))
            outf.write(tformat.format('total', self.amount, self.equity))


class PositionSnap:
    def __init__(self, date, net_value, equity, value_cost):
        self.date = date
        self.net_value = net_value
        self.equity = equity
        # 持仓金额
        self.amount = _around(equity * net_value, AMOUNT_DECIMALS)
        if value_cost == 0:
            value_cost = net_value
        # 持仓收益
        self.profit = _around((net_value - value_cost) * equity, AMOUNT_DECIMALS)
        # 持仓收益率
        self.profit_rate = _around((net_value - value_cost) / value_cost, RATE_DECIMALS)

    @property
    def average_cost(self):
        if self.equity == 0:
            cost = 0.0
        else:
            cost = self.amount / self.equity
        return _around(cost, VALUE_DECIMALS)


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
        return _around(cost, VALUE_DECIMALS)

    @property
    def profit(self):
        snap = self.position_histories[-1]
        position = Accumulation(snap.amount, snap.equity)
        total = self.acc_sell + position
        profit = _around(total.amount - self.acc_buy.amount, AMOUNT_DECIMALS)
        profit_rate = _around(profit / self.acc_buy.amount, RATE_DECIMALS)
        return profit, profit_rate

    def settle(self, date, net_value):
        """当天结算收益"""
        snap = PositionSnap(date, net_value, self.position_equity, self.acc_buy.average_cost)
        self.position_histories.append(snap)

    def buy(self, date, net_value, amount):
        """买入"""
        amount = _around(amount, AMOUNT_DECIMALS)
        equity = _around(amount / net_value, decimals=EQUITY_DECIMALS)
        delta = self.acc_buy.append(date, amount, equity)
        self.position_equity = _around(self.position_equity + equity, EQUITY_DECIMALS)
        return delta

    def sell(self, date, net_value, position):
        """赎回"""
        equity = _around(self.position_equity * position, decimals=EQUITY_DECIMALS)
        amount = _around(equity * net_value, AMOUNT_DECIMALS)
        delta = self.acc_sell.append(date, amount, equity)
        self.position_equity = _around(self.position_equity - equity, EQUITY_DECIMALS)
        return delta

    def write_positions(self, out_csv):
        with open(out_csv, 'w') as outf:
            outf.write('date,nav,equity,amount,profit,rate\n')
            tformat = '{:},{:.%df},{:.%df},{:.%df},{:.%df},{:.%d%%}\n' % (
                VALUE_DECIMALS, EQUITY_DECIMALS, AMOUNT_DECIMALS, AMOUNT_DECIMALS, RATE_DECIMALS - 2)
            for snap in self.position_histories:
                outf.write(tformat.format(snap.date,
                                          snap.net_value,
                                          snap.equity,
                                          snap.amount,
                                          snap.profit,
                                          snap.profit_rate))

    def write_total(self, out_csv):
        snap = self.position_histories[-1]
        position = Accumulation(snap.amount, snap.equity)
        total = self.acc_sell + position
        profit = total - self.acc_buy
        with open(out_csv, 'w') as outf:
            outf.write('stat,equity,amount,avg_cost\n')
            tformat = '{:},{:.%df},{:.%df},{:.%df}\n' % (EQUITY_DECIMALS, AMOUNT_DECIMALS, VALUE_DECIMALS)
            outf.write(tformat.format('buy', self.acc_buy.equity, self.acc_buy.amount, self.acc_buy.average_cost))
            outf.write(tformat.format('position', position.equity, position.amount, position.average_cost))
            outf.write(tformat.format('sell', self.acc_sell.equity, self.acc_sell.amount, self.acc_sell.average_cost))
            outf.write(tformat.format('total', total.equity, total.amount, total.average_cost))
            outf.write(tformat.format('profit', profit.equity, profit.amount, profit.average_cost))
            outf.write('\n')
            outf.write('kind,profit,rate\n')
            # strategy profit
            profit = _around(total.amount - self.acc_buy.amount, AMOUNT_DECIMALS)
            profit_rate = _around(profit / self.acc_buy.amount, RATE_DECIMALS)
            outf.write(f'strategy,{profit},{profit_rate:.2%}\n')
            # regular profit
            net_value = self.position_histories[-1].net_value
            profit = _around(net_value * self.acc_buy.equity - self.acc_buy.amount, AMOUNT_DECIMALS)
            profit_rate = _around(profit / self.acc_buy.amount, RATE_DECIMALS)
            outf.write(f'regular,{profit},{profit_rate:.2%}\n')
            # fund profit
            net_value_delta = self.position_histories[-1].net_value - self.position_histories[0].net_value
            profit = _around(net_value_delta * self.acc_buy.equity, AMOUNT_DECIMALS)
            profit_rate = _around(profit / self.acc_buy.amount, RATE_DECIMALS)
            outf.write(f'fund,{profit},{profit_rate:.2%}\n')
