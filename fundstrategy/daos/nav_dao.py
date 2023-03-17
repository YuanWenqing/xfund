# coding: utf8
from fundstrategy.core import sql_handler
from fundstrategy.core import models


class NavDao:
    def __init__(self, sql: sql_handler.SqlHandler):
        self.sql = sql

    def _row_to_nav(self, row: dict):
        return models.FundNav(date=row['value_date'],
                              value=row['unit_value'],
                              increase=row['increase_rate'])

    def insert_ignore(self, info: models.FundInfo, nav: models.FundNav):
        query = 'insert ignore into fund_nav' \
                '(code,name,value_date,unit_value,increase_rate,day_of_week,year_week)' \
                ' values(%s,%s,%s,%s,%s,weekday(%s)+1,yearweek(%s))'
        args = (info.code, info.name, nav.date, nav.value, nav.increase, nav.date, nav.date)
        self.sql.do_insert(query, args)

    def get_nav(self, code: str, date: str) -> models.FundNav:
        query = 'select * from fund_nav where code=%s and value_date=%s'
        args = [code, date]
        row = self.sql.do_select(query, args, size=None)
        return self._row_to_nav(row)

    def list_navs(self, code: str, start: str = None, end: str = None):
        query = 'select * from fund_nav where code=%s'
        args = [code]
        if start:
            query += ' and value_date>=%s'
            args.append(start)
        if end:
            query += ' and value_date<=%s'
            args.append(end)
        query += ' order by value_date asc'
        rows = self.sql.do_select(query, args, size=0)
        navs = [self._row_to_nav(r) for r in rows]
        return navs
