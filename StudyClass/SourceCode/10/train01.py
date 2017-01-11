# coding=utf-8

"""
地址的类PersonAddress。它的属性为：
    人员的姓名
    人员的电子信箱
拥有的方法：
    访问每个属性
    修改电子信箱地址
编写这个类，并实例化测试
"""
class PersonAddress(object):

    name = "LaoQi"
    email = "qiwsir@gmail.com"

    def aboutPerson(self):
        print "NAME:", PersonAddress.name
        print 'EMAIL:', PersonAddress.email

    def changeEmail(self, email):
        PersonAddress.email = email

p = PersonAddress()
p.aboutPerson()
p.changeEmail("canglaoshi@cang.lao")
p.aboutPerson()
