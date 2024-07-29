# coding: utf8
from xfund.daos import models
from xfund.strategies import profits
from xfund.strategies.regular import ProfitStrategy


class StopByProfitRate(ProfitStrategy):
    """根据收益率阈值止盈"""

    def __init__(self, profit_rate: float = 20 / 100):
        """
        :param profit_rate: 收益率阈值
        """
        self.profit_rate = profit_rate

    def do_strategy(self, record: profits.ProfitRecord, days: int, nav: models.FundNav):
        if record.position_profit_rate >= self.profit_rate:
            record.sell(nav.date,
                        net_value=nav.value,
                        equity=record.position_equity)
