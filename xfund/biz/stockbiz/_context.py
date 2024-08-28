# coding: utf8
from xfund.biz import beans
from xfund.biz._biz_context import BizContext
from xfund.biz.stockbiz._stock_info_dao import StockInfoDao
from xfund.biz.stockbiz._stock_kline_dao import StockKlineDao
from xfund.biz.stockbiz._stock_manager import StockManager


class StockContext(BizContext):

    @property
    @beans.bean
    def stock_info_dao(self) -> StockInfoDao:
        return StockInfoDao(self.sql)

    @property
    @beans.bean
    def stock_kline_dao(self) -> StockKlineDao:
        return StockKlineDao(self.sql)

    @property
    @beans.bean
    def stock_manager(self) -> StockManager:
        return StockManager(self)
