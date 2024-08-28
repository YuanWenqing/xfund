# coding: utf8
import abc


class SqlCond(abc.ABC):
    @abc.abstractmethod
    def sql(self) -> str:
        raise NotImplementedError

    @abc.abstractmethod
    def args(self) -> list:
        raise NotImplementedError


class FieldValueCmpCond(SqlCond, abc.ABC):
    """字段与值比较的条件"""

    def __init__(self, field: str, value):
        self.field = field
        self.value = value


class EqValueCond(FieldValueCmpCond):
    def sql(self) -> str:
        return f'{self.field}=%s'

    def args(self) -> list:
        return [self.value]


class NotEqValueCond(FieldValueCmpCond):
    def sql(self) -> str:
        return f'{self.field}!=%s'

    def args(self) -> list:
        return [self.value]


class GtValueCond(FieldValueCmpCond):
    def sql(self) -> str:
        return f'{self.field}>%s'

    def args(self) -> list:
        return [self.value]


class GteValueCond(FieldValueCmpCond):
    def sql(self) -> str:
        return f'{self.field}>=%s'

    def args(self) -> list:
        return [self.value]


class LtValueCond(FieldValueCmpCond):
    def sql(self) -> str:
        return f'{self.field}<%s'

    def args(self) -> list:
        return [self.value]


class LteValueCond(FieldValueCmpCond):
    def sql(self) -> str:
        return f'{self.field}<=%s'

    def args(self) -> list:
        return [self.value]


class IsNull(SqlCond):
    def __init__(self, field: str):
        self.field = field

    def sql(self) -> str:
        return f'{self.field} is Null'

    def args(self) -> list:
        return []


class IsNotNull(SqlCond):
    def __init__(self, field: str):
        self.field = field

    def sql(self) -> str:
        return f'{self.field} is NOT Null'

    def args(self) -> list:
        return []


class LikeCond(SqlCond):
    def __init__(self, field: str, pattern: str):
        self.field = field
        self.pattern = pattern

    def sql(self):
        return f'{self.field} like %s'

    def args(self):
        return [self.pattern]


class NotLikeCond(SqlCond):
    def __init__(self, field: str, pattern: str):
        self.field = field
        self.pattern = pattern

    def sql(self):
        return f'{self.field} not like %s'

    def args(self):
        return [self.pattern]


class RegexpCond(SqlCond):
    def __init__(self, field: str, pattern: str):
        self.field = field
        self.pattern = pattern

    def sql(self):
        return f'{self.field} regexp %s'

    def args(self):
        return [self.pattern]


class InCond(SqlCond):
    def __init__(self, field: str, values: list):
        self.field = field
        self.values = values

    def sql(self) -> str:
        in_sql = ','.join(['%s'] * len(self.values))
        return f'{self.field} in ({in_sql})'

    def args(self) -> list:
        return self.values
