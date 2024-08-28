# coding: utf8
import typing

import requests

from xfund import daos


class BaiduPae:
    """
    百度股市通接口
    """

    def list_stock_infos(self, offset: int = 0, page_size: int = 100) -> typing.List[daos.StockInfo]:
        """市值排序：大部分基金持仓的股票是大公司"""
        url = f'https://finance.pae.baidu.com/selfselect/getmarketrank?sort_type=1&sort_key=24&from_mid=1&pn={offset}&rn={page_size}&group=ranklist&type=ab&finClientType=pc'
        headers = {'content-type': 'application/json',
                   'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:22.0) Gecko/20100101 Firefox/22.0'}
        r = requests.get(url, headers=headers)
        data = r.json()
        data = data['Result']['Result']['DisplayData']['resultData']['tplData']['result']['rank']
        stocks = []
        for item in data:
            stock = daos.StockInfo(code=item['code'],
                                   name=item['name'],
                                   exchange=item['exchange'],
                                   market=item['market'],
                                   )
            stocks.append(stock)
        return stocks
