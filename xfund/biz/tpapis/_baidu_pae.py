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
        headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'accept-language': 'zh-CN,zh;q=0.9',
            'cache-control': 'no-cache',
            'pragma': 'no-cache',
            'priority': 'u=0, i',
            'sec-ch-ua': '"Not)A;Brand";v="99", "Google Chrome";v="127", "Chromium";v="127"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"macOS"',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'none',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36',
        }
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
