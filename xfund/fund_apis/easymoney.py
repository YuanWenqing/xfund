# coding: utf8
from xfund.fund_apis import fund_api
from xfund.core import models

import requests
import json
import re


class EastMoney(fund_api.FundApi):
    """
    https://cloud.tencent.com/developer/article/1695640
    """

    def get_nav_list(self, code: str, start_date: str = '', end_date: str = '') -> models.FundNavList:
        url = "http://fund.eastmoney.com/pingzhongdata/%s.js" % code
        headers = {'content-type': 'application/json',
                   'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:22.0) Gecko/20100101 Firefox/22.0'}
        r = requests.get(url, headers=headers)
        content = r.text
        name = re.findall(r'var fS_name = "([^"]+)";', content)[0]
        info = models.FundInfo(code, name)
        nav_list = models.FundNavList(info)
        data = re.findall(r'Data_netWorthTrend = ([^;]+);', content)[0]
        data = json.loads(data)
        for item in data:
            nav_list.append(date=models.fund_date(item['x'] / 1000),
                            value=item['y'],
                            increase=item['equityReturn'])
        return nav_list
