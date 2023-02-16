import os
import typing
from decimal import Decimal

from fundstrategy.core import accs
from fundstrategy.core import decimals


class PositionSnap:
    """
    持仓快照: 持仓资产、收益及成本价说明：https://www.futuhk.com/hans/support/topic448?lang=zh-cn
    """

    def __init__(self, date: str, net_value: Decimal, equity: Decimal, cost: Decimal):
        """
        :param date: 日期
        :param net_value: 当日净值
        :param equity: 持仓份额
        :param cost: 买入成本
        """
        self.date = date
        self.net_value = net_value
        self.equity = equity
        self.cost = cost

    @property
    def amount(self) -> Decimal:
        """持仓金额"""
        return decimals.amount(self.equity * self.net_value)

    @property
    def avg_value(self):
        """平均买入净值"""
        if self.equity == 0:
            return decimals.value(0)
        return decimals.value(self.cost / self.equity)

    @property
    def profit(self) -> Decimal:
        """持仓收益"""
        return self.amount - self.cost

    @property
    def profit_rate(self) -> Decimal:
        """持仓收益率"""
        if self.cost == 0:
            return decimals.rate(0)
        return decimals.rate(self.profit / self.cost)


class ProfitRecord:
    """收益记录"""

    def __init__(self):
        # 累计买入
        self.acc_buy = accs.Accumulation()
        # 累计卖出
        self.acc_sell = accs.Accumulation()
        # 持仓历史
        self.histories: typing.List[PositionSnap] = []
        # 当前持仓份额
        self._equity = decimals.equity(0)
        # 当前净值
        self._value = decimals.equity(0)

    @property
    def position_amount(self) -> Decimal:
        """当前持仓金额"""
        return decimals.amount(self._equity * self._value)

    @property
    def position_equity(self) -> Decimal:
        return self._equity

    @property
    def position_cost(self) -> Decimal:
        """当前持仓成本"""
        return self.acc_buy.amount - self.acc_sell.amount

    @property
    def position_diluted_value(self) -> Decimal:
        """当前持仓摊薄净值"""
        if self.position_equity == 0:
            value = 0
        else:
            value = self.position_cost / self.position_equity
        return decimals.value(value)

    @property
    def position_profit(self) -> Decimal:
        """当前持仓收益"""
        return self.position_amount - self.position_cost

    @property
    def position_profit_rate(self) -> Decimal:
        """当前持仓收益率"""
        if self.position_cost == 0:
            return decimals.rate(0)
        return decimals.rate(self.position_profit / self.position_cost)

    @property
    def total_amount(self) -> Decimal:
        """历史总金额=持仓金额+卖出金额"""
        return self.position_amount + self.acc_sell.amount

    @property
    def total_equity(self) -> Decimal:
        """历史总份额=持仓份额+卖出份额"""
        return self.position_equity + self.acc_sell.equity

    @property
    def total_cost(self) -> Decimal:
        """历史总成本"""
        return self.acc_buy.amount

    @property
    def total_profit(self) -> Decimal:
        """历史总收益"""
        return self.total_amount - self.total_cost

    @property
    def total_profit_rate(self) -> Decimal:
        """历史收益率"""
        if self.total_cost == 0:
            return decimals.rate(0)
        return decimals.rate(self.total_profit / self.total_cost)

    def buy(self, date: str, net_value: float, amount: float) -> accs.Delta:
        """买入"""
        delta = accs.Delta(date=date,
                           amount=decimals.amount(amount),
                           equity=decimals.equity(amount / net_value),
                           net_value=decimals.value(net_value),
                           )
        self.acc_buy.acc(delta)
        self._equity = self._equity + delta.equity
        return delta

    def sell(self, date: str, net_value: float,
             equity: typing.Union[float, Decimal] = None,
             amount: typing.Union[float, Decimal] = None) -> accs.Delta:
        """赎回"""
        assert not (equity is None and amount is None)
        if equity is None:
            equity = float(amount) / net_value
        else:
            amount = float(equity) * net_value
        delta = accs.Delta(date=date,
                           amount=decimals.amount(amount),
                           equity=decimals.equity(equity),
                           net_value=decimals.value(net_value),
                           )
        self.acc_sell.acc(delta)
        self._equity = self._equity - delta.equity
        return delta

    def settle(self, date: str, net_value: float) -> PositionSnap:
        """当天结算收益"""
        position = PositionSnap(date,
                                net_value=decimals.value(net_value),
                                equity=self.position_equity,
                                cost=self.position_cost,
                                )
        self.histories.append(position)
        self._value = decimals.value(net_value)
        return position

    def max_value_in_days(self, days: int) -> Decimal:
        """最近N天内的最大净值"""
        max_value = decimals.value(0)
        for position in self.histories[-days:]:
            max_value = max(max_value, position.net_value)
        return max_value

    def value_drawback_rate(self, curr_value: float, days: int) -> Decimal:
        """指定净值相对于最近N天最大净值的变动比例"""
        max_value = self.max_value_in_days(days)
        if max_value == 0:
            rate = 0
        else:
            rate = (max_value - decimals.value(curr_value)) / max_value
        return decimals.rate(rate)

    def write_positions(self, out_csv):
        os.makedirs(os.path.dirname(out_csv), exist_ok=True)
        with open(out_csv, 'w') as outf:
            outf.write('date,nav,equity,amount,cost,profit,rate\n')
            for snap in self.histories:
                outf.write(_csv_row(snap.date,
                                    snap.net_value,
                                    snap.equity,
                                    snap.amount,
                                    snap.cost,
                                    snap.profit,
                                    f'{snap.profit_rate:.2%}'))

    def write_total(self, out_csv):
        acc_position = accs.Accumulation(self.position_amount, self.position_equity)
        acc_total = accs.Accumulation(self.total_amount, self.total_equity)
        acc_profit = accs.Accumulation(self.total_profit, self.total_equity)
        with open(out_csv, 'w') as outf:
            # value
            outf.write('日期,净值,变动\n')
            beg, end = self.histories[0], self.histories[-1]
            outf.write(f'{beg.date},{beg.net_value},\n')
            change_rate = decimals.rate(end.net_value / beg.net_value - 1)
            outf.write(f'{end.date},{end.net_value},{change_rate:.2%}\n')
            outf.write(',\n')

            # outline
            outf.write('收益对比,收益,收益率\n')
            # 当前策略总收益
            outf.write(f'策略收益,{self.total_profit},{self.total_profit_rate:.2%}\n')
            # regular profit
            net_value = self.histories[-1].net_value
            profit = decimals.amount(net_value * self.acc_buy.equity - self.acc_buy.amount)
            profit_rate = decimals.rate(profit / self.acc_buy.amount)
            outf.write(f'定投收益,{profit},{profit_rate:.2%}\n')
            # fund profit
            equity = decimals.equity(self.acc_buy.amount / beg.net_value)
            profit = decimals.amount((end.net_value - beg.net_value) * equity)
            profit_rate = decimals.rate(profit / self.acc_buy.amount)
            outf.write(f'基金变动,{profit},{profit_rate:.2%}\n')
            outf.write(',\n')

            # acc
            outf.write('维度,份额,金额,平均净值\n')
            for name, acc in [
                ('买入累计', self.acc_buy),
                ('卖出累计', self.acc_sell),
                ('当前持仓', acc_position),
                ('历史投入', acc_total),
                ('历史收益', acc_profit),
            ]:
                outf.write(_csv_row(name, acc.equity, acc.amount, acc.average_value))
            outf.write('\n')


def _csv_row(*args):
    return ','.join([str(i) for i in args]) + '\n'
