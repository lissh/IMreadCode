
class Person(object):
    h=1.8
    def getName(self):
        print "My name is lish ."

    def color(self,col):
        print "The sky is {0}".format(col)

p= Person()
p.getName()
p.color("blue")

print p.h

p.a="hello"
print p.a