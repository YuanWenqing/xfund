# coding: utf8
# coding: utf8
import os
import typing
from decimal import Decimal

from fundstrategy.core import decimals


class Delta:
    """累加变动"""

    def __init__(self, date: str, amount: Decimal, equity: Decimal):
        self.date = date
        self.amount = amount
        self.equity = equity

    def __repr__(self):
        return f'<{self.__class__.__name__}: {self.date}, amount={self.amount:.2f}, equity={self.equity:.3f}>'


class Accumulation:
    """累加器"""

    def __init__(self, amount: Decimal = decimals.amount(0), equity: Decimal = decimals.equity(0)):
        self.amount = amount
        self.equity = equity
        self.histories: typing.List[Delta] = []

    def acc(self, date: str, amount: Decimal, equity: Decimal) -> Delta:
        """累加"""
        self.amount = self.amount + amount
        self.equity = self.equity + equity
        delta = Delta(date=date,
                      amount=amount,
                      equity=equity,
                      )
        self.histories.append(delta)
        return delta

    @property
    def average_value(self) -> Decimal:
        """平均净值"""
        if self.equity == 0:
            value = 0.0
        else:
            value = self.amount / self.equity
        return decimals.value(value)

    def write_history(self, out_csv):
        os.makedirs(os.path.dirname(out_csv), exist_ok=True)
        with open(out_csv, 'w') as outf:
            outf.write('date,amount,equity\n')
            tformat = '{:},{:},{:}\n'
            for item in self.histories:
                outf.write(tformat.format(item.date, item.amount, item.equity))
            outf.write(tformat.format('total', self.amount, self.equity))
