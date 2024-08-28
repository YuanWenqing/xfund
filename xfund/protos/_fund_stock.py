# coding: utf8
from xfund import sqls


class FundStock(sqls.SqlMessage):
    """基金持仓股票"""

    def __init__(self, *,
                 code: str = None,
                 name: str = None,
                 position_percent: str = None,
                 ):
        super().__init__()
        self.code = code
        self.name = name
        self.position_percent = position_percent
