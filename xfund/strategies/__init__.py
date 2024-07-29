# coding: utf8
from ._add_by_value_drawback import AddByValueDrawback
from ._add_by_value_increase import AddByValueIncrease
from ._stop_by_profit_rate import StopByProfitRate
from ._stop_by_value_drawback import StopByValueDrawback
from ._take_delta_profit import TakeDeltaProfit


def parse_strategy(conf: str):
    if ':' in conf:
        name, args = conf.split(':', maxsplit=1)
    else:
        name, args = conf, ''
    args = [float(i) for i in args.split(',') if i]
    cls = eval(f'{name}')
    return cls(*args)
