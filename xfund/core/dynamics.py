# coding: utf8
import json
import typing


class DynamicObject:
    def __init__(self, data: dict, strict=False):
        self._data_ = data
        self._strict_ = strict

    def unwrap(self) -> dict:
        return self._data_

    def __getattr__(self, item):
        if item not in self._data_:
            if self._strict_:
                raise AttributeError(f'unknown attribute: {item}')
            return None
        value = self._data_[item]
        if isinstance(value, dict):
            value = DynamicObject(value, strict=self._strict_)
        return value

    def __setitem__(self, key, value):
        self._data_[key] = value

    def __len__(self):
        return len(self._data_)

    def __repr__(self):
        return self._data_.__repr__()

    @staticmethod
    def parse_json(json_str: str, strict=False):
        d = json.loads(json_str)
        return DynamicObject(d, strict=strict)

    def as_json(self, indent: typing.Union[int, None] = 2):
        return json.dumps(self._data_, indent=indent, ensure_ascii=False)


def wrap(data, strict=False):
    if isinstance(data, dict):
        data = DynamicObject(data, strict=strict)
    elif isinstance(data, typing.Iterable):
        data = wrap_iterable_items(data, strict=strict)
    return data


def wrap_iterable_items(items: typing.Iterable, strict=False):
    new_items = []
    for i in items:
        if isinstance(i, dict):
            i = DynamicObject(i, strict=strict)
        new_items.append(i)
    new_items = type(items)(new_items)
    return new_items


def unwrap(data):
    if isinstance(data, DynamicObject):
        data = data.unwrap()
    elif isinstance(data, typing.Iterable):
        data = unwrap_iterable_items(data)
    return data


def unwrap_iterable_items(items: typing.Iterable):
    new_items = []
    for i in items:
        if isinstance(i, DynamicObject):
            i = i.unwrap()
        new_items.append(i)
    new_items = type(items)(new_items)
    return new_items


def jsonify(data, indent=2):
    data = unwrap(data)
    return json.dumps(data, indent=indent, ensure_ascii=False)
