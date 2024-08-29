# coding: utf8
from xfund.biz import beans
from xfund.biz._biz_context import BizContext
from xfund.biz.fundbiz._fund_manager import FundManager
from xfund.biz.fundbiz._fund_info_dao import FundInfoDao
from xfund.biz.fundbiz._fund_nav_dao import FundNavDao


class FundContext(BizContext):

    @property
    @beans.bean
    def fund_info_dao(self) -> FundInfoDao:
        return FundInfoDao(self.sql)

    @property
    @beans.bean
    def fund_nav_dao(self) -> FundNavDao:
        return FundNavDao(self.sql)

    @property
    @beans.bean
    def fund_manager(self) -> FundManager:
        return FundManager(self)
