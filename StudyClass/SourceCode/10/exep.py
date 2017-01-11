# coding = utf-8

class Person(object):
    """
    This is about a person.
    """
    def __init__(self, name, lang="python"):
        self.name = name
        self.lang = lang
        self.email = "qiwsir@gmail.com"
        
    def getName(self):
        return self.name

    def color(self, col):
        print "{0} is {1}".format(self.name, col)

laoqi = Person("qiwsir")
name = laoqi.getName()
print name
cang = Person("canglaoshi")
cang_name = cang.getName()
print cang_name
cang.color("white")
laoqi.color("black")

print cang.lang
print laoqi.lang
print cang.email
print laoqi.email
