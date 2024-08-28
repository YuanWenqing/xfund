# coding: utf8
from xfund import sqls
from xfund.biz import beans


class CoreContext(beans.BeanContext):
    """核心上下文：密钥、存储、数据库等"""

    @property
    @beans.bean
    def hostname(self):
        import socket
        return socket.gethostname()

    @property
    @beans.bean
    def sql_connection_factory(self) -> sqls.ConnectionFactory:
        mysql_url: str = 'mysql://fund:123456@localhost/fund'
        factory = sqls.ConnectionFactory.parse_url(mysql_url)
        return factory

    @property
    @beans.bean
    def sql_handler(self) -> sqls.SqlHandler:
        sql = sqls.SqlHandler(self.sql_connection_factory)
        self.logger.info(f'sql: {sql}')
        return sql
