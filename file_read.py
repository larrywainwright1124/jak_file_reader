from datetime import datetime
from decimal import Decimal

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
headerInfo = [{'tRecs': tRecs, 'tDebit': tDebit, 'tDebitAmt': tDebitAmt, 'tPay': tPay}]
"""

f = open("thefile.txt", "r")

"""
having difficulties understanding the parameters I need to put in
"""


def readfile(self, f):
    f = open('thefile.txt', "r")

    headerTrecs = int(self.tRecs)

    self.tRecs = f.read(6)
    self.tDebit = f.read(6)
    self.tPay = f.read(6)
    self.tDebitAmtRaw = f.read(12)
    self.tDebitAmt = float(int(self.tDebitAmtRaw) * .01)
    self.tPaysAmtRaw = f.read(12)
    self.tPayAmt = float(int(self.tPaysAmtRaw) * .01)

    self.index = f.read(6)
    self.tType = f.read(3)
    self.accNum = f.read(16)
    self.dateRaw = f.read(8)
    self.date = datetime(year=int(self.dateRaw[0:4]), month=int(self.dateRaw[4:6]), day=int(self.dateRaw[6:8]))
    self.name = f.read(25)
    self.city = f.read(23)
    self.state = f.read(2)
    self.acqCode = f.read(5)
    self.tAmountRaw = f.read(12)
    self.tAmount = int(self.tAmountRaw) * .01


