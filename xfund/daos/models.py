# coding: utf8
import time
import typing


class FundNav:
    def __init__(self, date: str, value: float, increase: float):
        """
        :param date: yyyy-MM-dd
        :param value: 净值
        :param increase: 日增长率的百分点，0.1 -> 0.1%
        """
        self.date = date
        self.value = value
        self.increase = increase

    def __repr__(self):
        return f'<{self.__class__.__name__}: {self.date}, {self.value}, {self.increase}>'

    @property
    def rate(self):
        return self.increase / 100

    @property
    def weekday(self):
        t = time.strptime(self.date, DATE_FORMAT)
        return t.tm_wday + 1


class FundNavList:
    def __init__(self, fund_info: FundInfo, nav_list: typing.List[FundNav] = None):
        self.info = fund_info
        self.nav_list = nav_list or []

    def __repr__(self):
        info = self.info.__repr__()
        tformat = '{:<10} {:>6} {:>6}'
        navs = [tformat.format(i.date, i.value, i.increase) for i in self.nav_list]
        navs = '\n'.join(navs)
        return f'{info}\nnavs:\n{navs}'

    def __len__(self):
        return len(self.nav_list)

    def append(self, date: str, value: float, increase: float):
        self.nav_list.append(FundNav(date, value, increase))


DATE_FORMAT = '%Y-%m-%d'


def fund_date(ts: float):
    t = time.localtime(ts)
    date = time.strftime(DATE_FORMAT, t)
    return date
