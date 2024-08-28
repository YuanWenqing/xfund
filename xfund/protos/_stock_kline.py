# coding: utf8

from xfund import sqls


class StockKline(sqls.SqlMessage):
    """股票K线行情"""

    def __init__(self, *,
                 code: str = None,
                 name: str = None,
                 date: str = None,
                 open_price: str = None,
                 close_price: str = None,
                 high_price: str = None,
                 low_price: str = None,
                 volume: int = None,
                 ):
        super().__init__()
        self.key = f'{code}@{date}'
        self.code = code
        self.name = name
        self.date = date
        self.open_price = open_price
        self.close_price = close_price
        self.high_price = high_price
        self.low_price = low_price
        self.volume = volume
