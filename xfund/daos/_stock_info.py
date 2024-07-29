# coding: utf8
import typing

from xfund.core import sqls
from xfund.core.sqls import SqlHandler


class StockInfo(sqls.SqlMessage):
    """股票信息"""

    def __init__(self, *,
                 code: str = None,
                 name: str = None,
                 ):
        super().__init__()
        self.code = code
        self.name = name


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
                ]

    def get_stock(self, code: str) -> StockInfo:
        assert code
        return self.get_message_by_key(code)
