# coding: utf8
from fundstrategy.core import models
from fundstrategy.core import profits
from fundstrategy.core.regular import ProfitStrategy


class TakeDeltaProfit(ProfitStrategy):
    """根据收益率阈值提取超额收益"""

    def __init__(self, profit_rate: float = 20 / 100):
        """
        :param profit_rate: 收益率阈值
        """
        self.profit_rate = profit_rate

        self._prefix_rate = 0

    def do_strategy(self, record: profits.ProfitRecord, days: int, nav: models.FundNav):
        if record.position_profit_rate >= self._prefix_rate + self.profit_rate:
            record.sell(nav.date,
                        net_value=nav.value,
                        amount=record.position_profit)
            self._prefix_rate += self.profit_rate
