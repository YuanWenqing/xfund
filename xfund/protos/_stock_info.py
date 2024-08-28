# coding: utf8

from xfund import sqls


class StockInfo(sqls.SqlMessage):
    """股票信息"""

    def __init__(self, *,
                 code: str = None,
                 name: str = None,
                 exchange: str = None,  # 交易市场代码
                 market: str = None,  # 市场，ab中国A股
                 ):
        super().__init__()
        self.code = code
        self.name = name
        self.exchange = exchange
        self.market = market
