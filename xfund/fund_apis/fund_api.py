# coding: utf8
import abc

from xfund.core import models


class FundApi(abc.ABC):
    @abc.abstractmethod
    def get_nav_list(self, code: str, start_date: str = '', end_date: str = '') -> models.FundNavList:
        raise NotImplementedError
