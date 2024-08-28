# coding: utf8
from xfund.biz import beans
from xfund.biz._biz_context import BizContext
from xfund.biz.tpapis._baidu_pae import BaiduPaeApi
from xfund.biz.tpapis._east_money import EastMoneyApi
from xfund.biz.tpapis._sina_finance import SinaFinanceApi


class TpApiContext(BizContext):
    """第三方api"""

    @property
    @beans.bean
    def baidu_pae_api(self) -> BaiduPaeApi:
        return BaiduPaeApi()

    @property
    @beans.bean
    def east_money_api(self) -> EastMoneyApi:
        return EastMoneyApi()

    @property
    @beans.bean
    def sina_finance_api(self) -> SinaFinanceApi:
        return SinaFinanceApi()
