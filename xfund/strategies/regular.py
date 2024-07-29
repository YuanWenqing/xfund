# coding: utf8
import abc
import logging
import re
import typing

import numpy as np

from xfund.daos import models
from xfund.strategies import profits


class ProfitStrategy(abc.ABC):
    """收益率策略"""

    @abc.abstractmethod
    def do_strategy(self, record: profits.ProfitRecord, days: int, nav: models.FundNav):
        """策略操作"""
        raise NotImplemented


class RegularInvest:
    """定投"""

    def __init__(self,
                 init_amount: float,
                 interval: str,
                 delta_amount: float,
                 decrease: str = None,
                 strategies: typing.List[ProfitStrategy] = None
                 ):
        """
        :param init_amount: 初始建仓金额
        :param interval: 定投间隔
        :param delta_amount: 定投金额
        :param decrease: 定投金额递减配置，<rate_grid>:<decrease_amount>
        """
        self.logger = logging.getLogger(self.__class__.__name__)

        self.init_amount = init_amount
        self.interval = parse_interval(interval)
        self.delta_amount = delta_amount
        self.decrease = parse_decrease(decrease)
        self.strategies = strategies or []

    def backtest(self, navs: typing.List[models.FundNav]) -> profits.ProfitRecord:
        """历史回测"""
        record = profits.ProfitRecord()
        for i, nav in enumerate(navs):
            if i == 0:
                # 初始建仓
                record.buy(nav.date, nav.value, self.init_amount)
            else:
                self.do_strategies(record, i, nav)
                self.do_regular(record, i, nav)
            record.settle(nav.date, nav.value)
        return record

    def do_regular(self, record: profits.ProfitRecord, days: int, nav: models.FundNav):
        """定投操作"""
        amount = self.delta_amount
        if self.decrease and record.position_profit_rate > 0:
            k = int(np.floor(float(record.position_profit_rate) / self.decrease[0]))
            amount -= self.decrease[1] * k
        if amount <= 0:
            return
        if self.interval[0] == 'day' and days % self.interval[1] == 0:
            record.buy(nav.date, nav.value, amount)
        elif self.interval[0] == 'week' and nav.weekday == self.interval[1]:
            record.buy(nav.date, nav.value, amount)

    def do_strategies(self, record: profits.ProfitRecord, days: int, nav: models.FundNav):
        """策略操作"""
        for s in self.strategies:
            s.do_strategy(record, days, nav)


def parse_interval(interval: str):
    m = re.match('^d(\d+)$', interval)
    if m:
        return 'day', int(m.group(1))
    m = re.match('^w([1-5])$', interval)
    if m:
        return 'week', int(m.group(1))
    raise ValueError(interval)


def parse_decrease(decrease: str):
    if decrease:
        rate, amount = [float(i) for i in decrease.split(':')]
        assert rate > 0 and amount > 0
        return rate, amount
    return None
