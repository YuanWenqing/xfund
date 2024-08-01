# coding: utf8
import typing

from xfund.core import sqls
from xfund.core.sqls import SqlHandler


class FundNav(sqls.SqlMessage):
    """基金净值 NAV(NetAssetValue)"""

    def __init__(self, *,
                 code: str = None,
                 name: str = None,
                 date: str = None,
                 net_price: float = None,
                 delta_percent: float = None,
                 ):
        super().__init__()
        self.key = f'{code}@{date}'
        self.code = code
        self.name = name
        self.date = date
        self.net_price = net_price
        self.delta_percent = delta_percent


class FundNavDao(sqls.MessageDao[FundNav]):

    def __init__(self, sql: SqlHandler):
        super().__init__(FundNav, sql)

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

    def list_navs(self, code: str) -> typing.List[FundNav]:
        assert code
        return self.list_by_cond(cond_dict=dict(code=code))
