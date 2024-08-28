# coding: utf8
import typing

from xfund import protos
from xfund import sqls


class StockKlineDao(sqls.MessageDao[protos.StockKline]):

    def __init__(self, sql: sqls.SqlHandler):
        super().__init__(protos.StockKline, sql)

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

    def list_klines(self, code: str) -> typing.List[protos.StockKline]:
        assert code
        return self.list_by_cond(cond_dict=dict(code=code))
