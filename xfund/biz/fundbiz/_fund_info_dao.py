# coding: utf8
import typing

from xfund import protos
from xfund import sqls
from xfund.sqls import SqlHandler


class FundInfoDao(sqls.MessageDao[protos.FundInfo]):

    def __init__(self, sql: SqlHandler):
        super().__init__(protos.FundInfo, sql)

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

    def get_fund(self, code: str) -> protos.FundInfo:
        assert code
        return self.get_message_by_key(code)
