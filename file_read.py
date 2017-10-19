"""
What I want to do is create a class that is to read the whole document
But I think that means that I need to create a class, and then subclasses underneath that do the following:
    1st - Read the header and then put it into a data structure
    2nd - Read the document
    3rd - Check to make sure that the values in the header match the values in the document
        if they do -
            put all data into the data structure
        if they dont -
            return and error saying so
I dont think the following is the right way to put the information into a dictionary ? I don't really know how to output the key - value pairs in the dictionary "headerinfo"
I also dont know
"""
"""
having difficulties understanding the parameters I need to put in
"""

"""
headerInfo = [{'tRecs': tRecs, 'tDebit': tDebit, 'tDebitAmt': tDebitAmt, 'tPay': tPay}]
"""

from datetime import datetime
from decimal import Decimal


class Readheader:
    def __init__(self,):
        i = 0
        f = open('thefile.txt', "r")
        while i < self.tRec * 9:
            self.tRecsStr = f.read(6)
            self.tRec = int(self.tRecsStr)
            self.tDebitStr = f.read(6)
            self.tPayStr = f.read(6)
            self.tDebitAmtStr = f.read(12)
            self.tDebitAmt = float(int(self.tDebitAmtStr) * .01)
            self.tPaysAmtStr = f.read(12)
            self.tPayAmt = float(int(self.tPaysAmtStr) * .01)

            self.index = f.read(6)
            self.tType = f.read(3)
            self.accNum = f.read(16)
            self.dateRaw = f.read(8)
            self.date = datetime(year=int(self.dateRaw[0:4]), month=int(self.dateRaw[4:6]), day=int(self.dateRaw[6:8]))
            self.name = f.read(25)
            self.city = f.read(23)
            self.state = f.read(10)
            self.acqCode = f.read(5)
            self.tAmountRaw = f.read(12)
            self.tAmount = int(self.tAmountRaw) * .01
            self.n = '\n'

            record = [self.index, self.name, self.tType, self.accNum, self.date, self.city, self.state, self.acqCode, self.tAmount, self.n]
            for item in record:
                print (item)
                i = i + 1






