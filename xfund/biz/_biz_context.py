# coding: utf8
import abc

from xfund import sqls
from xfund.biz import beans
from xfund.biz._core_context import CoreContext


class BizContext(beans.BeanContext, abc.ABC):
    def __init__(self, core: CoreContext, parent: beans.BeanContext):
        super().__init__(parent=parent)
        self.core_ctx = core

    @property
    def sql(self) -> sqls.SqlHandler:
        return self.core_ctx.sql_handler
