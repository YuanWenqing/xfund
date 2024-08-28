# coding: utf8
import abc
import json


class SqlMessage(abc.ABC):
    """数据库表对象"""

    def __init__(self):
        pass

    def as_dict(self) -> dict:
        d = self.__dict__
        return d

    def json_dumps(self) -> str:
        return json.dumps(self.as_dict())

    @classmethod
    def json_loads(cls, s: str):
        d: dict = json.loads(s)
        m = cls()
        for k, v, in d.items():
            if hasattr(m, k):
                setattr(m, k, v)
        return m
