# coding: utf8
import typing

from xfund.core import sqls
from xfund.core.sqls import SqlHandler


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


class StockKlineDao(sqls.MessageDao[StockKline]):

    def __init__(self, sql: SqlHandler):
        super().__init__(StockKline, sql)

    @property
    def table(self) -> str:
        return 'stock_kline'

    @property
    def key_field(self) -> str:
        return 'key'

    @property
    def column_fields(self) -> typing.List[str]:
        return ['key',
                'code',
                'name',
                'date',
                'open_price',
                'close_price',
                'high_price',
                'low_price',
                'volume',
                ]

    def list_klines(self, code: str) -> typing.List[StockKline]:
        assert code
        return self.list_by_cond(cond_dict=dict(code=code))
