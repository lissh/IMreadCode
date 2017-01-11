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

    def query(self,vars_hql,hql,callback):
        try:
            transport = TSocket.TSocket(self.host,self.port)
            transport = TTransport.TBufferedTransport(transport)
            protocol = TBinaryProtocol.TBinaryProtocol(transport)
            client = ThriftHive.Client(protocol)
            transport.open()
            #获取表的字段名列表
            # vars_hql='desc dmn.us_am_uid_class'
            client.execute(vars_hql)

            rows=[str(row) for row in client.fetchAll()]
            i=0
            isOver=False
            vars_name=[]
            while isOver==False:
                row=rows[i]
                if  '\t \t ' in str(row):
                    isOver=True
                vars_name+=[row.split('\t')[0].replace(' ','')]
                i+=1
            vars_name=vars_name[0:-1]

            #获取表中的数据记录
            # hql = 'select * from dmn.us_am_uid_class limit 5'
            client.execute(hql)

            records=[]
            for row in  client.fetchAll():
                record={}
                j=0
                conts =row.split('\t')
                # print conts
                for cont in conts:
                    key=vars_name[j]
                    record[key]=cont
                    # print cont
                    j+=1
                records+=[record]
            # print records
            transport.close()
            callback(records)

        except Thrift.TException, tx:
            callback(None)
            print '%s' % (tx.message)