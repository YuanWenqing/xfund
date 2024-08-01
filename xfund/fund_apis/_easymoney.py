# coding: utf8
import json
import re
import time
import typing

import requests

from xfund import daos


class EastMoneyApi:
    """
    天天基金接口
    https://cloud.tencent.com/developer/article/1695640
    https://blog.csdn.net/begin_python/article/details/126982865
    https://www.cnblogs.com/insane-Mr-Li/p/15378971.html
    """

    def get_nav_list(self, code: str, start_date: str = '', end_date: str = '') -> typing.List[daos.FundNav]:
        url = "http://fund.eastmoney.com/pingzhongdata/%s.js" % code
        headers = {'content-type': 'application/json',
                   'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:22.0) Gecko/20100101 Firefox/22.0'}
        r = requests.get(url, headers=headers)
        content = r.text
        name = re.findall(r'var fS_name = "([^"]+)";', content)[0]
        data = re.findall(r'Data_netWorthTrend = ([^;]+);', content)[0]
        data = json.loads(data)
        navs = []
        for item in data:
            nav = daos.FundNav(code=code,
                               name=name,
                               date=fund_date(item['x'] / 1000),
                               net_price=item['y'],
                               delta_percent=item['equityReturn'],
                               )
            navs.append(nav)
        return navs


DATE_FORMAT = '%Y-%m-%d'


def fund_date(ts: float):
    t = time.localtime(ts)
    date = time.strftime(DATE_FORMAT, t)
    return date
