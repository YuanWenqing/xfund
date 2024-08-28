# coding: utf8
import logging
import typing

import tqdm


class StockManager:
    """管理股票信息和行情数据"""

    def __init__(self, ctx):
        self.logger = logging.getLogger(self.__class__.__name__)

        from xfund.biz.stockbiz._context import StockContext
        self.ctx = typing.cast(StockContext, ctx)
        self.stock_info_dao = self.ctx.stock_info_dao
        self.stock_kline_dao = self.ctx.stock_kline_dao

    def import_all_stocks(self):
        from xfund.biz._serving_context import ServingContext
        ctx = typing.cast(ServingContext, self.ctx.parent_ctx)
        pae_api = ctx.tpapi_context.baidu_pae_api
        all_stocks = []
        offset, page_size = 0, 100
        while True:
            stocks = pae_api.list_stock_infos(offset=offset, page_size=page_size)
            if len(stocks) == 0:
                break
            all_stocks.extend(stocks)
            offset += page_size
        for stock in tqdm.tqdm(all_stocks):
            self.stock_info_dao.insert_message(stock, insert_ignore=True)
        return stocks
