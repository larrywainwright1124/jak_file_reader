from datetime import datetime, timedelta
from db import DB
from random import randrange


class Data:
    """
    Takes data set up in the class properties and creates a string that is used to write to file.
    """
    def __init__(self):
        self.index = 1
        self.transaction_type = 0
        self.transaction_date = None
        self.acct_nbr = ''
        self.merchant_name = ''
        self.merchant_city = ''
        self.merchant_state = ''
        self.acq_id = ''
        self.amount = 0

    def to_string(self):
        """
        Builds the out string.  Notice the names in {} in the out string and notice the call to format
        and how that works.  This is good stuff to know.
        :return:
        """
        out = "{idx}{type}{acct}{date}{name}{city}{state}{acqid}{amt}"
        out = out.format(idx=str(self.index).zfill(6), type=self.transaction_type,
                         date=self.transaction_date.strftime('%Y%m%d'),
                         acct=self.acct_nbr, name=self.merchant_name, city=self.merchant_city,
                         state=self.merchant_state, acqid=self.acq_id,
                         amt=str(int(self.amount*100)).zfill(12))
        return out


class DataWriter:
    """
    Creates the thefile.txt file.
    """
    def __init__(self):
        with open('data/adjectives.txt', 'r') as f:
            self.adj = f.read().splitlines()
        with open('data/nouns.txt') as f:
            self.noun = f.read().splitlines()
        with open('data/verbs.txt') as f:
            self.verb = f.read().splitlines()
        self.states = ['AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DL', 'DC', 'FL', 'GA', 'HI', 'ID',
                       'IL', 'IN', 'IA', 'KA', 'KY', 'LA', 'ME', 'MD', 'MA', 'MI', 'MN', 'MS', 'MO',
                       'MT', 'NE', 'NV', 'NH', 'NJ', 'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA',
                       'RI', 'SC', 'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY']
        self.city = ['Danbury', 'Great Bridge', 'Tompkinsville', 'Burke', 'Pelham', 'Knoxville',
                     'Pleasant Farms', 'Saunders', 'Fordham', 'Dhaka', 'Decatur', 'Pontiac',
                     'Santiago', 'Gatewood', 'Daly City', 'San Rafael', 'Cheektowaga', 'Palatine']
        self.max_records = 150

        self.total_pmts = 0
        self.total_debits = 0
        self.total_sum_pmts = 0
        self.total_sum_debits = 0

        self.db = DB('walgreens', 'root', 'root')

    def build_merchant_name(self):
        adj_idx = randrange(0, len(self.adj)-1)
        noun_idx = randrange(0, len(self.noun)-1)
        verb_idx = randrange(0, len(self.verb)-1)

        str = self.adj[adj_idx] + ' ' + self.noun[noun_idx] + ' ' + self.verb[verb_idx]
        str = str.upper()
        if len(str) > 25:
            str = str[0:25]
        elif len(str) < 25:
            str = str.ljust(25)
        return str

    def get_state(self):
        return self.states[randrange(0, len(self.states)-1)]

    def get_city(self):
        city = self.city[randrange(0, len(self.city)-1)]
        city = city.upper()
        if len(city) > 23:
            city = city[0:23]
        elif len(city) < 23:
            city = city.ljust(23)
        return city

    def get_acq_id(self):
        id = str(randrange(1, 9))
        for _ in range(1, 5):
            id += str(randrange(0, 9))
        return id

    def random_amount(self):
        d = str(randrange(10, 110))
        c = str(randrange(11, 99))
        dollars = float(d + '.' + c)
        # cents = int(dollars * 100)
        # result = str(cents).zfill(12)
        # return result
        return dollars

    def random_account(self):
        sql = "select card_number from ac_card order by rand() limit 1"
        return self.db.fetch_col('card_number', sql)
        # result = '4785'
        # while len(result) != 16:
        #     result += str(randrange(0, 9))
        # return result

    def random_type(self):
        types = [520, 522, 527, 620, 622, 627]
        return types[randrange(0, len(types)-1)]

    def random_date(self):
        days = randrange(1, 10)
        dt = datetime.now() - timedelta(days=days)
        # return dt.strftime('%Y%m%d')
        return dt

    def build_line(self, row_index):
        out = "{idx}{type}{acct}{date}{name}{city}{state}{acqid}{amt}\n"
        idx = str(row_index).zfill(6)
        type = self.random_type()
        acct = self.random_account()
        dt = self.random_date()
        name = self.build_merchant_name()
        city = self.get_city()
        state = self.get_state()
        acqid = self.get_acq_id()
        amt = self.random_amount()
        return out.format(idx=idx, type=type, acct=acct, date=dt, name=name,
                          city=city, state=state, acqid=acqid, amt=amt)

    def write_file(self):
        list = []
        for idx in range(0, self.max_records):
            d = Data()
            d.acq_id = self.get_acq_id()
            d.amount = self.random_amount()
            d.index = idx + 1
            d.transaction_type = self.random_type()
            d.transaction_date = self.random_date()
            d.acct_nbr = self.random_account()
            d.merchant_name = self.build_merchant_name()
            d.merchant_city = self.get_city()
            d.merchant_state = self.get_state()
            if d.transaction_type in [520, 522, 527]:
                self.total_debits += 1
                self.total_sum_debits += d.amount
            elif d.transaction_type in [620, 622, 627]:
                self.total_pmts += 1
                self.total_sum_pmts += d.amount
            list.append(d)

        header = str(len(list)).zfill(6) + str(self.total_debits).zfill(6) +\
                 str(self.total_pmts).zfill(6) +\
                 str(int(self.total_sum_debits*100)).zfill(12) +\
                 str(int(self.total_sum_pmts*100)).zfill(12)
        with open('thefile.txt', 'w') as f:
            f.write(header)
            # print len(header)
            for d in list:
                # print len(d.to_string())
                f.write(d.to_string())


if __name__ == '__main__':
    dw = DataWriter()
    dw.write_file()


