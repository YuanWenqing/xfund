# coding: utf8
import logging
import typing

from fundstrategy.core import models
from fundstrategy.strategies import profits


class WaveRegularStrategy:
    def __init__(self,
                 init_amount: float,
                 regular_days: int,
                 regular_amount: float,
                 take_profit_rate: float,
                 take_profit_position: float,
                 add_position_rate: float,
                 add_position_amount: float,
                 # stop_loss_rate: float,
                 ):
        """

        :param init_amount: 初始建仓金额
        :param regular_days: 定投间隔日期
        :param regular_amount: 定投金额
        :param take_profit_rate: 止盈收益率
        :param take_profit_position: 止盈仓位比例
        :param add_position_rate: 加仓收益率（抄底）
        :param add_position_amount: 加仓金额
        # :param stop_loss_rate: 止损收益率，全部赎回
        """
        self.init_amount = init_amount
        self.regular_days = regular_days
        self.regular_amount = regular_amount
        self.take_profit_rate = take_profit_rate
        self.take_profit_position = take_profit_position
        self.add_position_rate = add_position_rate
        self.add_position_amount = add_position_amount
        # self.stop_loss_rate = stop_loss_rate

        self.logger = logging.getLogger(self.__class__.__name__)

    def backtest(self, navs: typing.List[models.FundNav]) -> profits.ProfitRecord:
        record = profits.ProfitRecord()
        for i, nav in enumerate(navs):
            if i == 0:
                # 初始建仓
                record.buy(nav.date, nav.value, self.init_amount)
            else:
                position = record.position_histories[-1]
                if position.profit_rate >= self.take_profit_rate:
                    delta = record.sell(nav.date, nav.value, self.take_profit_position)
                    self.logger.info(
                        f'profit_rate={position.profit_rate:.2%} > {self.take_profit_rate:.2%}: sell {delta}')
                if (i + 1) % self.regular_days == 0:
                    record.buy(nav.date, nav.value, self.regular_amount)
            record.settle(nav.date, nav.value)
        return record
