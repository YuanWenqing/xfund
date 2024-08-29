# coding: utf8
import logging
import typing


class FundManager:
    """管理基金信息和行情数据"""

    def __init__(self, ctx):
        self.logger = logging.getLogger(self.__class__.__name__)

        from xfund.biz.fundbiz._context import FundContext
        self.ctx = typing.cast(FundContext, ctx)
        self.fund_info_dao = self.ctx.fund_info_dao
        self.fund_nav_dao = self.ctx.fund_nav_dao

        from xfund.biz._serving_context import ServingContext
        ctx = typing.cast(ServingContext, self.ctx.parent_ctx)
        self.east_money_api = ctx.tpapi_context.east_money_api

    def update_fund_navs(self, code):
        navs = self.east_money_api.get_nav_list(code)
        if len(navs) == 0:
            return navs
        for nav in navs:
            self.fund_nav_dao.insert_message(nav, insert_ignore=True)
        return navs
