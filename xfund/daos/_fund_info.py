# coding: utf8
import typing

from xfund.core import sqls
from xfund.core.sqls import SqlHandler


class FundInfo(sqls.SqlMessage):
    """基金信息"""

    def __init__(self, *,
                 code: str = None,
                 name: str = None,
                 stock_codes: typing.List[str] = (),
                 ):
        super().__init__()
        self.code = code
        self.name = name
        self.stock_codes = stock_codes


class FundInfoDao(sqls.MessageDao[FundInfo]):

    def __init__(self, sql: SqlHandler):
        super().__init__(FundInfo, sql)

    @property
    def table(self) -> str:
        return 'fund_info'

    @property
    def key_field(self) -> str:
        return 'code'

    @property
    def column_fields(self) -> typing.List[str]:
        return ['code',
                'name',
                ]

    def get_fund(self, code: str) -> FundInfo:
        assert code
        return self.get_message_by_key(code)
