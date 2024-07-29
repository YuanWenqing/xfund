# coding: utf8
import typing
from decimal import Decimal


def equity(v: typing.Union[float, Decimal]) -> Decimal:
    v = float(v)
    return Decimal.from_float(v).quantize(Decimal('.001'))


def value(v: typing.Union[float, Decimal]) -> Decimal:
    v = float(v)
    return Decimal.from_float(v).quantize(Decimal('.0001'))


def amount(v: typing.Union[float, Decimal]) -> Decimal:
    v = float(v)
    return Decimal.from_float(v).quantize(Decimal('.01'))


def rate(v: typing.Union[float, Decimal]) -> Decimal:
    v = float(v)
    return Decimal.from_float(v).quantize(Decimal('.0001'))
