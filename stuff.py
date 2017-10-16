
class stuff:
    def __init__(self):
        self.x = 10

    def runme(self):
        print self.x


obj = stuff()
print "this is reference to objects x value: ", obj.x
print "now we call the objects runme method which prints self.x: ",
obj.runme()

