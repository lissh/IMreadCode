# -*- coding=utf-8 -*-
#!/bin/env python
__author__ = 'lish'
from hive_service import ThriftHive
from hive_service.ttypes import HiveServerException
from thrift import Thrift
from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol


class hiveDB():
    def __init__(self, _host, _port):
        self.host = _host
        self.port = _port

    def query(self,hsql,callback):
        try:
            transport = TSocket.TSocket(self.host,self.port)
            transport = TTransport.TBufferedTransport(transport)
            protocol = TBinaryProtocol.TBinaryProtocol(transport)
            client = ThriftHive.Client(protocol)
            transport.open()
            #获取表中的数据记录
            client.execute(hsql)
            callback(client.fetchAll())
            transport.close()


        except Thrift.TException, tx:
            callback(None)
            print '%s' % (tx.message)


#
# app=hiveDB('182.92.183.76',9084)
# app.query()