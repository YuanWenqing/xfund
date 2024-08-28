# coding: utf8
# coding: utf8
import typing

from xfund import protos
from xfund import sqls


class StockInfoDao(sqls.MessageDao[protos.StockInfo]):

    def __init__(self, sql: sqls.SqlHandler):
        super().__init__(protos.StockInfo, sql)

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

    def get_stock(self, code: str) -> protos.StockInfo:
        assert code
        return self.get_message_by_key(code)
