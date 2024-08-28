# coding: utf8
import typing

from xfund import protos
from xfund import sqls
from xfund.sqls import SqlHandler


class FundNavDao(sqls.MessageDao[protos.FundNav]):

    def __init__(self, sql: SqlHandler):
        super().__init__(protos.FundNav, sql)

    @property
    def table(self) -> str:
        return 'fund_nav'

    @property
    def key_field(self) -> str:
        return 'key'

    @property
    def column_fields(self) -> typing.List[str]:
        return ['key',
                'code',
                'name',
                'date',
                'net_price',
                'delta_percent',
                ]

    def list_navs(self, code: str) -> typing.List[protos.FundNav]:
        assert code
        return self.list_by_cond(cond_dict=dict(code=code))
