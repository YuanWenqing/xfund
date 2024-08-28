# coding: utf8
from xfund.biz import beans
from xfund.biz import fundbiz
from xfund.biz import stockbiz
from xfund.biz import tpapis


class ServingContext(beans.BeanContext):

    @property
    @beans.bean
    def fund_context(self) -> fundbiz.FundContext:
        return fundbiz.FundContext(core=self.core_ctx, parent=self)

    @property
    @beans.bean
    def stock_context(self) -> stockbiz.StockContext:
        return stockbiz.StockContext(core=self.core_ctx, parent=self)

    @property
    @beans.bean
    def tpapi_context(self) -> tpapis.TpApiContext:
        return tpapis.TpApiContext(core=self.core_ctx, parent=self)
