# coding: utf8
import typing

from xfund import sqls
from xfund.sqls import SqlHandler


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


class StockInfoDao(sqls.MessageDao[StockInfo]):

    def __init__(self, sql: SqlHandler):
        super().__init__(StockInfo, sql)

    @property
    def table(self) -> str:
        return 'stock_info'

    @property
    def key_field(self) -> str:
        return 'code'

    @property
    def column_fields(self) -> typing.List[str]:
        return ['code',
                'name',
                'exchange',
                'market',
                ]

    def get_stock(self, code: str) -> StockInfo:
        assert code
        return self.get_message_by_key(code)
