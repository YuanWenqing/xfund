# coding: utf8
from fundstrategy.core import models
from fundstrategy.core import profits
from fundstrategy.core.regular import ProfitStrategy


class StopByValueDrawback(ProfitStrategy):
    """根据净值回撤比例止盈"""

    def __init__(self,
                 drawback_days: int,
                 drawback_rate: float):
        """
        :param drawback_days: 回撤计算天数
        :param drawback_rate: 回撤比例阈值
        """
        assert drawback_rate < 0
        self.drawback_days = drawback_days
        self.drawback_rate = drawback_rate

    def do_strategy(self, record: profits.ProfitRecord, days: int, nav: models.FundNav):
        rate = record.value_drawback_rate(nav.value, days=self.drawback_days)
        if rate <= self.drawback_rate:
            record.sell(nav.date,
                        net_value=nav.value,
                        equity=record.position_equity)
