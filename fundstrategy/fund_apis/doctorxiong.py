# coding: utf8
import enum
import logging

import requests as requests

from fundstrategy.core import dynamics
from fundstrategy.fund_apis import fund_api
from fundstrategy.core import models


class ErrCode(enum.Enum):
    OK = 200


class DoctorXiong(fund_api.FundApi):
    """
    https://www.doctorxiong.club/api/#api-Fund-getFundDetail
    """

    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)

    def do_get(self, url):
        resp = requests.get(url)
        resp = dynamics.DynamicObject.parse_json(resp.text)
        self.logger.info(f'{url} --> {resp}')
        return resp

    def get_fund_detail(self, code: str, start_date: str = '', end_date: str = ''):
        url = f'https://api.doctorxiong.club/v1/fund/detail?code={code}&startDate={start_date}&endDate={end_date}'
        return self.do_get(url)

    def get_nav_list(self, code: str, start_date: str = '', end_date: str = '') -> models.FundNavList:
        detail = self.get_fund_detail(code, start_date, end_date).data
        fund_info = models.FundInfo(detail.code, detail.name)
        nav_list = models.FundNavList(fund_info)
        for item in detail.netWorthData:
            nav_list.append(date=item[0],
                            value=item[1],
                            increase=item[2])
        return nav_list
