# coding: utf8
from xfund.core import models
from xfund.core import profits
from xfund.core.regular import ProfitStrategy


class AddByValueIncrease(ProfitStrategy):
    """根据当日净值回撤比例加仓"""

    def __init__(self,
                 increase_rate: float = -2 / 100,
                 add_amount: float = 10_000):
        """
        :param increase_rate: 当日净值变动比例阈值
        :param add_amount: 加仓金额
        """
        self.increase_rate = increase_rate
        self.add_amount = add_amount

    def do_strategy(self, record: profits.ProfitRecord, days: int, nav: models.FundNav):
        if nav.rate <= self.increase_rate:
            record.buy(nav.date,
                       net_value=nav.value,
                       amount=self.add_amount)
