# coding: utf8
import typing

from xfund.core.sqls._sql_conds import SqlCond


def cond_of_dict(cond_dict: dict) -> (str, typing.List):
    """条件字典构建条件语句"""
    cond_sql = ' and '.join([f'{k}=%s' for k in cond_dict.keys()])
    cond_args = list(cond_dict.values())
    return cond_sql, cond_args


def cond_of_multi(conds: typing.List[SqlCond]) -> (str, typing.List):
    """抽象条件列表构建条件语句"""
    cond_sqls = []
    cond_args = []
    for cond in conds:
        cond_sqls.append(cond.sql())
        cond_args.extend(cond.args())
    cond_sql = ' and '.join(cond_sqls)
    return cond_sql, cond_args
