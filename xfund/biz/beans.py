# coding: utf8
import functools
import logging
import typing


class BeanContext:
    def __init__(self, parent=None):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.beans = {}
        self.parent_ctx = parent


def bean(function):
    @functools.wraps(function)
    def find_bean(*args, **kwargs):
        name = function.__name__
        ctx: BeanContext = args[0]
        if hasattr(ctx, 'logger'):
            logger = getattr(ctx, 'logger')
        else:
            logger = logging
        # search bean
        chain = find_ctx_chain(ctx)
        for c in chain:
            if name in c.beans:
                value = c.beans[name]
                logger.debug(f'found bean {name} in {c}: {value}')
                return value
        # create and populate
        value = function(*args, **kwargs)
        if name in ctx.beans and value == ctx.beans[name]:
            # bean may be created in sub context and populated to this context
            # no need to populate again
            logger.debug(f'found bean {name} in {ctx}: {value}')
            return value
        logger.debug(f'{ctx} create bean {name}: {value}')
        for c in chain:
            c.beans[name] = value
        return value

    return find_bean


def find_ctx_chain(ctx: BeanContext) -> typing.List[BeanContext]:
    chain = [ctx]
    while True:
        if ctx.parent_ctx:
            ctx = ctx.parent_ctx
            chain.append(ctx)
        else:
            break
    return chain
