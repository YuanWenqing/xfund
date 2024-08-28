# coding: utf8
import logging
import typing

from xfund.biz.fundbiz._context import FundContext


class FundManager:
    """管理基金信息和行情数据"""

    def __init__(self, ctx):
        self.logger = logging.getLogger(self.__class__.__name__)

        ctx = typing.cast(FundContext, ctx)
        self.fund_info_dao = ctx.fund_info_dao
        self.fund_nav_dao = ctx.fund_nav_dao
