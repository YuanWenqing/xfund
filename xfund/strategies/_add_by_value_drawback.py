# coding: utf8
from xfund.core import models
from xfund.core import profits
from xfund.core.regular import ProfitStrategy


class AddByValueDrawback(ProfitStrategy):
    """根据近期回撤比例加仓"""

    def __init__(self,
                 drawback_days: int = 5,
                 drawback_rate: float = -10 / 100,
                 add_amount: float = 10_000):
        """
        :param drawback_days: 回撤计算天数
        :param drawback_rate: 回撤比例阈值
        :param add_amount: 加仓金额
        """
        assert drawback_rate < 0
        self.drawback_days = int(drawback_days)
        self.drawback_rate = drawback_rate
        self.add_amount = add_amount

    def do_strategy(self, record: profits.ProfitRecord, days: int, nav: models.FundNav):
        rate = record.value_drawback_rate(nav.value, days=self.drawback_days)
        if rate <= self.drawback_rate:
            record.buy(nav.date,
                       net_value=nav.value,
                       amount=self.add_amount)
