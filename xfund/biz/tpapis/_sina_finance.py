# coding: utf8
import typing

import requests

from xfund import protos


class SinaFinanceApi:
    """
    新浪财经接口
    """

    def list_stock_kline(self, code) -> typing.List[protos.StockKline]:
        url = f'http://money.finance.sina.com.cn/quotes_service/api/json_v2.php/CN_MarketData.getKLineData?symbol={code}&scale=240&datalen=1023'
        headers = {'content-type': 'application/json',
                   'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:22.0) Gecko/20100101 Firefox/22.0'}
        r = requests.get(url, headers=headers)
        data = r.json()
        klines = []
        for item in data:
            kline = protos.StockKline(code=code,
                                    date=item['day'],
                                    open_price=item['open'],
                                    close_price=item['close'],
                                    high_price=item['high'],
                                    low_price=item['low'],
                                    volume=int(item['volume']),
                                    )
            klines.append(kline)
        return klines
