# coding: utf8

from xfund import sqls


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
        self.pk = f'{code}@{date}'
        self.code = code
        self.name = name
        self.date = date
        self.net_price = net_price
        self.delta_percent = delta_percent
