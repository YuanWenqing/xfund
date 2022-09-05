# coding: utf8
import time


class FundInfo:
    def __init__(self, code, name):
        self.code = code
        self.name = name


class FundNav:
    def __init__(self, date: str, value: float, increase: float):
        """
        :param date: yyyy-MM-dd
        :param value:
        :param increase:
        """
        self.date = date
        self.value = value
        self.increase = increase


class FundNavList:
    def __init__(self, fund_info: FundInfo, nav_list=None):
        if nav_list is None:
            nav_list = []
        self.fund_info = fund_info
        self.nav_list = nav_list

    def append(self, date: str, value: float, increase: float):
        self.nav_list.append(FundNav(date, value, increase))


DATE_FORMAT = '%Y-%m-%d'


def fund_date(ts: float):
    t = time.localtime(ts)
    date = time.strftime(DATE_FORMAT, t)
    return date
