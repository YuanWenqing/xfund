# coding: utf8
import typing

from xfund import sqls


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
