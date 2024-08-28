# coding: utf8
import logging
import typing

import requests

from xfund import protos


class BaiduPaeApi:
    """
    百度股市通接口
    """

    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)

    def list_stock_infos(self, offset: int = 0, page_size: int = 100) -> typing.List[protos.StockInfo]:
        """市值排序：大部分基金持仓的股票是大公司"""
        url = f'https://finance.pae.baidu.com/selfselect/getmarketrank?sort_type=1&sort_key=24&from_mid=1&pn={offset}&rn={page_size}&group=ranklist&type=ab&finClientType=pc'
        headers = {'content-type': 'application/json',
                   'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:22.0) Gecko/20100101 Firefox/22.0'}
        self.logger.info(f'list_stock_infos: {url}')
        r = requests.get(url, headers=headers)
        self.logger.info(f'response: {r.text}')
        data = r.json()
        if data['ResultCode'] != '0':
            raise IOError(r.text)
        data = data['Result']['Result']['DisplayData']['resultData']['tplData']['result']['rank']
        stocks = []
        for item in data:
            stock = protos.StockInfo(code=item['code'],
                                     name=item['name'],
                                     exchange=item['exchange'],
                                     market=item['market'],
                                     )
            stocks.append(stock)
        return stocks
