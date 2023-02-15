# coding: utf8
from fundstrategy.core import models
from fundstrategy.core import profits
from fundstrategy.core.regular import ProfitStrategy


class AddByValueIncrease(ProfitStrategy):
    """根据净值回撤比例加仓"""

    def __init__(self,
                 increase_rate: float,
                 add_amount: float):
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
