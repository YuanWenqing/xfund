# coding: utf8
import enum
import logging

import requests as requests

from fundstrategy.core import dynamics


class ErrCode(enum.Enum):
    OK = 200


class DoctorXiong:
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
