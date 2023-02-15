import os
import typing
from decimal import Decimal

from fundstrategy.core import accs
from fundstrategy.core import decimals


class PositionSnap:
    """
    持仓快照: 持仓资产、收益及成本价说明：https://www.futuhk.com/hans/support/topic448?lang=zh-cn
    """

    def __init__(self, date: str, net_value: Decimal, equity: Decimal, avg_value: Decimal):
        """
        :param date: 日期
        :param net_value: 当日净值
        :param equity: 持仓份额
        :param avg_value: 平均买入净值
        """
        self.date = date
        self.net_value = net_value
        self.equity = equity
        self.avg_value = avg_value or net_value

    @property
    def amount(self) -> Decimal:
        """持仓金额"""
        return decimals.amount(self.equity * self.net_value)

    @property
    def profit(self) -> Decimal:
        """持仓收益"""
        return decimals.amount((self.net_value - self.avg_value) * self.equity)

    @property
    def profit_rate(self) -> Decimal:
        """持仓收益率"""
        return decimals.rate((self.net_value - self.avg_value) / self.avg_value)


class ProfitRecord:
    """收益记录"""

    def __init__(self):
        # 累计买入
        self.acc_buy = accs.Accumulation()
        # 累计卖出
        self.acc_sell = accs.Accumulation()
        # 持仓历史
        self.position_histories: typing.List[PositionSnap] = []
        # 当前持仓份额
        self.position_equity = decimals.equity(0)

    @property
    def position_amount(self) -> Decimal:
        """当前持仓金额"""
        if len(self.position_histories) == 0:
            return decimals.amount(0)
        return self.position_histories[-1].amount

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
        if len(self.position_histories) == 0:
            return decimals.equity(0)
        return self.position_histories[-1].profit

    @property
    def position_profit_rate(self) -> Decimal:
        """当前持仓收益率"""
        if len(self.position_histories) == 0:
            return decimals.equity(0)
        return self.position_histories[-1].profit_rate

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
        self.position_equity = self.position_equity + delta.equity
        return delta

    def sell(self, date: str, net_value: float, equity: float) -> accs.Delta:
        """赎回"""
        delta = accs.Delta(date=date,
                           amount=decimals.amount(equity * net_value),
                           equity=decimals.equity(equity),
                           net_value=decimals.value(net_value),
                           )
        self.acc_sell.acc(delta)
        self.position_equity = self.position_equity - delta.equity
        return delta

    def settle(self, date: str, net_value: float) -> PositionSnap:
        """当天结算收益"""
        position = PositionSnap(date,
                                net_value=decimals.value(net_value),
                                equity=self.position_equity,
                                avg_value=self.acc_buy.average_value)
        self.position_histories.append(position)
        return position

    def drawback(self, days: int) -> Decimal:
        """回撤比例"""
        max_value = decimals.value(0)
        for position in self.position_histories[-days:-1]:
            max_value = max(max_value, position.net_value)
        cur_value = self.position_histories[-1].net_value
        if max_value == 0:
            rate = 0
        else:
            rate = (max_value - cur_value) / max_value
        return decimals.rate(rate)

    def write_positions(self, out_csv):
        os.makedirs(os.path.dirname(out_csv))
        with open(out_csv, 'w') as outf:
            outf.write('date,nav,equity,amount,profit,rate\n')
            for snap in self.position_histories:
                outf.write(_csv_row(snap.date,
                                    snap.net_value,
                                    snap.equity,
                                    snap.amount,
                                    snap.profit,
                                    snap.profit_rate))

    def write_total(self, out_csv):
        acc_position = accs.Accumulation(self.position_amount, self.position_equity)
        acc_total = accs.Accumulation(self.total_amount, self.total_equity)
        acc_profit = accs.Accumulation(self.total_profit, self.total_equity)
        with open(out_csv, 'w') as outf:
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

            outf.write(',收益,收益率\n')
            # 当前策略总收益
            outf.write(f'策略收益,{self.total_profit},{self.total_profit_rate:.2%}\n')
            # regular profit
            net_value = self.position_histories[-1].net_value
            profit = decimals.amount(net_value * self.acc_buy.equity - self.acc_buy.amount)
            profit_rate = decimals.rate(profit / self.acc_buy.amount)
            outf.write(f'定投收益,{profit},{profit_rate:.2%}\n')
            # fund profit
            net_value_delta = self.position_histories[-1].net_value - self.position_histories[0].net_value
            profit = decimals.amount(net_value_delta * self.acc_buy.equity)
            profit_rate = decimals.rate(profit / self.acc_buy.amount)
            outf.write(f'基金变动,{profit},{profit_rate:.2%}\n')


def _csv_row(*args):
    return ','.join([str(i) for i in args]) + '\n'
