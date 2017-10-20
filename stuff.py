from datetime import datetime, timedelta

class stuff:
    def __init__(self):
        self.x = 10

    def runme(self):
        print self.x


obj = stuff()
print "this is reference to objects x value: ", obj.x
print "now we call the objects runme method which prints self.x: ",
obj.runme()

print '\nlist all properties of an object:'
print dir(obj)
print '\nnow list all properties of an object that arent built in'
print 'also is example of a list comprehension that is too complicated for you to look at right now'
print 'but, good to keep in mind for later'
print [x for x in dir(obj) if x[:2] != '__' and x[:-2] != '__']
raw_input('press enter to continue')

# arrays, they can hold anything and different data types in them if necessary but that isn't very common
arr = ['this', 'is', 'an', 'array', 10, 20]
print '\nprinting array: ', arr
# loop thru array
for el in arr:
    print el
raw_input('press enter to continue')
print '-' * 80

# loop thru array and get index at same time also
# introduction to string format function
print '\nloop array getting both value and its index using enumerate function'
for idx, el in enumerate(arr):
    print 'Array element {idx} contains value: {value}'.format(idx=idx, value=el)
raw_input('press enter to continue')
print '-' * 80


# date creation, date math and dictionary
print '\ndate creation, date math and dictionary'
mydate = datetime.now() - timedelta(days=4)
print 'today - 4 is: ', mydate
raw_input('press enter to continue')

d = {'name': 'shithead', 'value': 'asshole', 'dt': mydate}
print '\ndump the whole dictionary out:'
print d
print 'printing a value for name from the dictionary: ', d['name']
print 'iterate over a dictionary:'
for key in d:
    print key

print '\nnotice, no values? that requires one of 2 techniques:'
raw_input('press enter to continue')
for key in d:
    print 'key: ', key, 'value: ', d[key]

raw_input('press enter to continue')

print '\nother technique (and more commonly used):'
for key, value in d.iteritems():
    print 'key: ', key, 'value: ', value


class FileReader:
    def __init__(self):
        with file('thefile.txt', 'r') as f:
            header = self.get_header_line(f)
            line = self.get_record(f)
            while line:
                print line
                line = self.get_record(f)
                
    def get_header_line(self, f):
        line = f.read(35)
        return line
    
    def get_record(self, f):
        line = f.read(55)
        return line
    
