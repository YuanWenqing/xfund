# coding: utf8
import logging
import typing

from fundstrategy.core import models
from fundstrategy.strategies import profits


class TakeProfitStrategy:
    def __init__(self,
                 init_amount: float,
                 regular_days: int,
                 regular_amount: float,
                 add_position_rate: float,
                 add_position_amount: float,

                 take_profit_rate: float,
                 take_profit_position: float,
                 ):
        """

        :param init_amount: 初始建仓金额
        :param regular_days: 定投间隔日期
        :param regular_amount: 定投金额
        :param add_position_rate: 加仓收益率（抄底）
        :param add_position_amount: 加仓金额
        :param take_profit_rate: 止盈收益率
        :param take_profit_position: 止盈仓位比例
        """
        self.init_amount = init_amount
        self.regular_days = regular_days
        self.regular_amount = regular_amount
        self.add_position_rate = add_position_rate
        self.add_position_amount = add_position_amount

        self.take_profit_rate = take_profit_rate
        self.take_profit_position = take_profit_position

        self.logger = logging.getLogger(self.__class__.__name__)

    def backtest(self, navs: typing.List[models.FundNav]) -> profits.ProfitRecord:
        record = profits.ProfitRecord()
        take_rate = self.take_profit_rate
        for i, nav in enumerate(navs):
            if i == 0:
                # 初始建仓
                record.buy(nav.date, nav.value, self.init_amount)
            else:
                profit_rate = nav.value / record.acc_buy.average_cost - 1
                if profit_rate > take_rate:
                    delta = record.sell(nav.date, nav.value, self.take_profit_position)
                    self.logger.info(f'profit_rate={profit_rate:.2%} > {take_rate:.2%}: sell {delta}')
                    take_rate += self.take_profit_rate
                elif nav.increase / 100 < self.add_position_rate:
                    delta = record.buy(nav.date, nav.value, self.add_position_amount)
                    self.logger.info(f'nav_increase={nav.increase:.2}% < {self.add_position_rate:.2%}: buy {delta}')
                if (i + 1) % self.regular_days == 0:
                    record.buy(nav.date, nav.value, self.regular_amount)
            record.settle(nav.date, nav.value)
        return record
