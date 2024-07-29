# coding: utf8
import abc
import logging
import typing

import tqdm
from pymysql import cursors

from xfund.core.sqls import sqlutil
from xfund.core.sqls._sql_conds import SqlCond
from xfund.core.sqls._sql_handler import SqlHandler
from xfund.core.sqls._sql_message import SqlMessage

MT = typing.TypeVar('MT', bound=SqlMessage)


class MessageDao(typing.Generic[MT], abc.ABC):
    FIELD_PAYLOAD = 'json_payload'

    def __init__(self, message_type: typing.Type[MT], sql: SqlHandler):
        self.logger = logging.getLogger(self.__class__.__name__)

        self.message_type = message_type
        self.sql = sql

    @property
    @abc.abstractmethod
    def table(self) -> str:
        """表名"""
        pass

    @property
    @abc.abstractmethod
    def key_field(self) -> str:
        """主键字段"""
        pass

    @property
    @abc.abstractmethod
    def column_fields(self) -> typing.List[str]:
        """列字段"""
        pass

    @property
    def auto_increment_field(self) -> typing.Optional[str]:
        """自增ID字段"""
        return None

    def parse_row(self, row: dict) -> typing.Optional[MT]:
        if row is None:
            return None
        payload = row.get(self.FIELD_PAYLOAD, None)
        if payload:
            message = self.message_type.json_loads(payload)
        else:
            message = self.message_type()
        for f in self.column_fields:
            if f in row and row[f] is not None:
                # field结果覆盖payload
                setattr(message, f, row[f])
        return message

    def parse_rows(self, rows: typing.List[dict]):
        return [self.parse_row(r) for r in rows]

    def cond_dict_of_message(self, message: MT) -> dict:
        return {self.key_field: getattr(message, self.key_field)}

    def _get_column_values(self, message: MT, ignore_fields=()) -> (list, list):
        columns, values = [], []
        for f in self.column_fields:
            if f in ignore_fields:
                continue
            v = getattr(message, f)
            columns.append(f)
            values.append(v)
        columns.append(self.FIELD_PAYLOAD)
        values.append(message.json_dumps())
        return columns, values

    def replace_message(self, message: MT):
        """替换message：插入 OR 更新"""
        cond = self.cond_dict_of_message(message)
        olds = self.list_by_cond(cond_dict=cond)
        if len(olds) == 0:
            self.insert_message(message)
            return 1
        else:
            self.update_message(message)
            return 0

    def insert_message(self, message: MT, insert_ignore=False):
        columns, args = self._get_column_values(message, ignore_fields=[self.auto_increment_field])
        column_sql = ','.join(columns)
        value_sql = ('%s,' * len(args))[:-1]
        if insert_ignore:
            query = 'insert ignore'
        else:
            query = 'insert'
        query = f'{query} into {self.table}({column_sql}) values({value_sql});'
        self.sql.do_insert(query, args)

    def get_message_by_key(self, key_value) -> MT:
        """根据主键获取message"""
        cond = {self.key_field: key_value}
        cond_sql, cond_args = sqlutil.build_cond_sql(cond)
        query = f'select * from {self.table} where {cond_sql};'
        row = self.sql.do_select(query, cond_args, size=None)
        message = self.parse_row(row)
        return message

    def list_messages(self, cond_sql: str = None, cond_args=None,
                      size: int = 0, offset: int = 0,
                      order_by: typing.Union[list, str] = None) -> typing.List[MT]:
        """
        根据条件语句获取message列表
        :param cond_sql:
        :param cond_args:
        :param size: 0：全部；>=1：size个
        :param offset:
        :param order_by: ['a asc','b desc'] or 'a asc, b desc'
        :return:
        """
        assert size is not None
        query = f'select * from {self.table}'
        if cond_sql:
            query += f' where {cond_sql}'
        if order_by:
            if isinstance(order_by, list):
                order_by = ','.join(order_by)
            query += f' order by {order_by}'
        if size > 0:
            query += f' limit {offset},{size}'
        args = cond_args
        rows = self.sql.do_select(query, args, size=size)
        messages = []
        for row in rows:
            messages.append(self.parse_row(row))
        return messages

    def list_by_cond(self, *, cond_dict: dict = None, conds: typing.List[SqlCond] = None) -> typing.List[MT]:
        """根据条件获取message列表"""
        if cond_dict is not None:
            cond_sql, cond_args = sqlutil.cond_of_dict(cond_dict)
        elif conds is not None:
            cond_sql, cond_args = sqlutil.cond_of_multi(conds)
        else:
            cond_sql, cond_args = '', []
        return self.list_messages(cond_sql, cond_args)

    def update_message(self, message, *, cond_dict: dict = None, conds: typing.List[SqlCond] = None) -> int:
        """更新message"""
        if cond_dict is not None:
            assert len(cond_dict) > 0
            cond_sql, cond_args = sqlutil.cond_of_dict(cond_dict)
        elif conds is not None:
            assert len(conds) > 0
            cond_sql, cond_args = sqlutil.cond_of_multi(conds)
        else:
            cond_dict = self.cond_dict_of_message(message)
            cond_sql, cond_args = sqlutil.cond_of_dict(cond_dict)
        set_fields, set_args = self._get_column_values(message, ignore_fields=[self.key_field])
        set_sql = ','.join([f'{f}=%s' for f in set_fields])
        query = f'update {self.table} set {set_sql} where {cond_sql}'
        args = set_args + cond_args
        return self.sql.do_update(query, args)

    def update_fields(self, sets: dict, *, cond_dict: dict = None, conds: typing.List[SqlCond] = None) -> int:
        """根据条件更新字段"""
        assert len(sets) > 0 and (cond_dict is not None or conds is not None)
        if cond_dict is not None:
            assert len(cond_dict) > 0
            cond_sql, cond_args = sqlutil.cond_of_dict(cond_dict)
        else:
            assert len(conds) > 0
            cond_sql, cond_args = sqlutil.cond_of_multi(conds)
        set_sql = ','.join([f'{f}=%s' for f in sets.keys()])
        set_args = list(sets.values())
        query = f'update {self.table} set {set_sql} where {cond_sql}'
        args = set_args + cond_args
        return self.sql.do_update(query, args)

    def delete_messages(self, cond_sql: str = None, cond_args=None) -> int:
        """删除messages"""
        cond_sql = cond_sql or '1'
        query = f'delete from {self.table} where {cond_sql}'
        return self.sql.do_delete(query, cond_args)

    def delete_by_cond(self, *, cond_dict: dict = None, conds: typing.List[SqlCond] = None) -> int:
        """根据条件删除message"""
        assert cond_dict is not None or conds is not None
        if cond_dict is not None:
            assert len(cond_dict) > 0
            cond_sql, cond_args = sqlutil.cond_of_dict(cond_dict)
        else:
            assert len(conds) > 0
            cond_sql, cond_args = sqlutil.cond_of_multi(conds)
        return self.delete_messages(cond_sql, cond_args)

    def iterate_message(self, cond_sql: str = None, cond_args=None,
                        page_size: int = 500, progress=True) -> typing.Iterable[MT]:
        """分页遍历"""

        def next_batch_cond():
            if last_key:
                if cond_sql:
                    batch_sql = f'{cond_sql} and {self.key_field}>%s'
                    batch_args = list(cond_args) + [last_key]
                else:
                    batch_sql = f'{self.key_field}>%s'
                    batch_args = [last_key]
            else:
                batch_sql = cond_sql
                batch_args = cond_args
            return batch_sql, batch_args

        assert page_size > 0
        if progress:
            total = self.count(cond_sql, cond_args)
        else:
            total = 0
        cond_args = cond_args or []
        last_key = None
        with tqdm.tqdm(total=total, desc=f'iterate {self.table}', disable=not progress) as progress:
            while True:
                next_sql, next_args = next_batch_cond()
                messages = self.list_messages(next_sql, next_args,
                                              size=page_size, offset=0,
                                              order_by=f'{self.key_field} asc')
                if len(messages) == 0:
                    break
                for message in messages:
                    progress.update(1)
                    yield message
                    last_key = getattr(message, self.key_field)

    def iterate_by_cond(self, *, cond_dict: dict = None, conds: typing.List[SqlCond] = None) -> typing.Iterable[MT]:
        """根据条件遍历message"""
        assert cond_dict is not None or conds is not None
        if cond_dict is not None:
            assert len(cond_dict) > 0
            cond_sql, cond_args = sqlutil.cond_of_dict(cond_dict)
        else:
            assert len(conds) > 0
            cond_sql, cond_args = sqlutil.cond_of_multi(conds)
        return self.iterate_message(cond_sql, cond_args)

    def count_messages(self, cond_sql: str = None, cond_args=None) -> int:
        """message计数"""
        query = f'select count(1) as cnt from {self.table}'
        if cond_sql:
            query += f' where {cond_sql}'
        row = self.sql.do_select(query, cond_args, cursorclass=cursors.DictCursor, size=None)
        if row is None:
            return 0
        return row['cnt']

    def count_by_cond(self, *, cond_dict: dict = None, conds: typing.List[SqlCond] = None) -> int:
        """根据条件计数message"""
        assert cond_dict is not None or conds is not None
        if cond_dict is not None:
            assert len(cond_dict) > 0
            cond_sql, cond_args = sqlutil.cond_of_dict(cond_dict)
        else:
            assert len(conds) > 0
            cond_sql, cond_args = sqlutil.cond_of_multi(conds)
        return self.count_messages(cond_sql, cond_args)
