# coding: utf8
import logging
import typing

from fundstrategy.core import models
from fundstrategy.core import profits


class Regular:
    """定投"""

    def __init__(self,
                 init_amount: float,
                 regular_days: int,
                 regular_amount: float,
                 ):
        """
        :param init_amount: 初始建仓金额
        :param regular_days: 定投间隔日期
        :param regular_amount: 定投金额
        """
        self.logger = logging.getLogger(self.__class__.__name__)

        self.init_amount = init_amount
        self.regular_days = regular_days
        self.regular_amount = regular_amount

    def backtest(self, navs: typing.List[models.FundNav]) -> profits.ProfitRecord:
        """历史回测"""
        record = profits.ProfitRecord()
        for i, nav in enumerate(navs):
            if i == 0:
                # 初始建仓
                record.buy(nav.date, nav.value, self.init_amount)
            else:
                self.do_strategy(record, i, nav)
                self.do_regular(record, i, nav)
            record.settle(nav.date, nav.value)
        return record

    def do_regular(self, record: profits.ProfitRecord, days: int, nav: models.FundNav):
        """定投操作"""
        if days and days % self.regular_days == 0:
            record.buy(nav.date, nav.value, self.regular_amount)

    def do_strategy(self, record: profits.ProfitRecord, days: int, nav: models.FundNav):
        """策略操作"""
        pass
