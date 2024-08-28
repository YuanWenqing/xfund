# coding: utf8
import logging
import typing

from xfund.biz.stockbiz._context import StockContext


class StockManager:
    """管理股票信息和行情数据"""

    def __init__(self, ctx):
        self.logger = logging.getLogger(self.__class__.__name__)

        ctx = typing.cast(StockContext, ctx)
        self.stock_info_dao = ctx.stock_info_dao
        self.stock_kline_dao = ctx.stock_kline_dao
