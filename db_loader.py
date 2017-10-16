from db import DB
from datetime import date
from random import randrange

TOTAL_RECORDS = 100


class DbLoader:
    """
    Create the database, walgreens and the tables it will populate or that will be used elsewhere.
    """

    def __init__(self):
        """
        Constructor
        """
        # instantiate the DB class and connect to the sys database using the root user/pwd.  This needs to
        # be changed if root has a different password.
        self.db = DB('sys', 'root', 'root')
        # load arrays with data from various files.
        with open('data/adjectives.txt', 'r') as f:
            self.adj = f.readlines()
        with open('data/nouns.txt') as f:
            self.noun = f.readlines()
        with open('data/verbs.txt') as f:
            self.verb = f.readlines()
        with open('data/first_names.txt') as f:
            self.first_names = f.readlines()
        with open('data/last_names.txt') as f:
            self.last_names = f.readlines()

        self.states = ['AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DL', 'DC', 'FL', 'GA', 'HI', 'ID',
                       'IL', 'IN', 'IA', 'KA', 'KY', 'LA', 'ME', 'MD', 'MA', 'MI', 'MN', 'MS', 'MO',
                       'MT', 'NE', 'NV', 'NH', 'NJ', 'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA',
                       'RI', 'SC', 'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY']
        self.city = ['Danbury', 'Great Bridge', 'Tompkinsville', 'Burke', 'Pelham', 'Knoxville',
                     'Pleasant Farms', 'Saunders', 'Fordham', 'Dhaka', 'Decatur', 'Pontiac',
                     'Santiago', 'Gatewood', 'Daly City', 'San Rafael', 'Cheektowaga', 'Palatine']

    def create_database(self):
        """
        Creates the database walgreens and then switches to it.
        :return: None
        """
        sql = "CREATE DATABASE IF NOT EXISTS walgreens /*!40100 DEFAULT CHARACTER SET utf8 */"
        self.db.execute(sql)
        self.db.select_database('walgreens')

    def create_tables(self):
        """
        Creates an array of scripts that create tables and then executes each.
        :return: None
        """
        tables = {}
        tables['ac_account'] = """
            CREATE TABLE IF NOT EXISTS  ac_account (
              xid INT NOT NULL AUTO_INCREMENT,
              bal_id INT NOT NULL DEFAULT 0,
              client_id INT NOT NULL DEFAULT 0,
              status VARCHAR(1) NOT NULL DEFAULT 'N',
              PRIMARY KEY (xid))
            ENGINE = InnoDB
            DEFAULT CHARACTER SET = utf8
        """

        tables['ac_balance'] = """
            CREATE TABLE IF NOT EXISTS ac_balance (
              bal_id INT NOT NULL AUTO_INCREMENT,
              open_to_buy DECIMAL(10,2) NOT NULL DEFAULT 0,
              cred_lim DECIMAL(10,2) NOT NULL DEFAULT 0,
              PRIMARY KEY (bal_id))
            ENGINE = InnoDB
            DEFAULT CHARACTER SET = utf8
        """

        tables['ac_card'] = """
            CREATE TABLE IF NOT EXISTS ac_card (
              cad INT NOT NULL AUTO_INCREMENT,
              xid INT NOT NULL DEFAULT 0,
              card_number VARCHAR(20) NOT NULL,
              expiry_date DATETIME NULL,
              card_status VARCHAR(1) NOT NULL DEFAULT 'N',
              PRIMARY KEY (cad))
            ENGINE = InnoDB
            DEFAULT CHARACTER SET = utf8;
        """

        tables['ac_client'] = """
            CREATE TABLE IF NOT EXISTS ac_client (
              client_id INT NOT NULL AUTO_INCREMENT,
              fname VARCHAR(50) NULL,
              lname VARCHAR(50) NULL,
              addr1 VARCHAR(50) NULL,
              addr2 VARCHAR(50) NULL,
              city VARCHAR(25) NULL,
              state VARCHAR(10) NULL,
              zip VARCHAR(5) NULL,
              PRIMARY KEY (client_id))
            ENGINE = InnoDB
            DEFAULT CHARACTER SET = utf8
        """

        tables['tp_trans'] = """
            CREATE TABLE IF NOT EXISTS tp_trans (
              trans_id INT NOT NULL AUTO_INCREMENT,
              trans_type VARCHAR(5) NOT NULL,
              account_nbr VARCHAR(20) NULL,
              in_ts DATETIME NULL,
              merch_name VARCHAR(25) NULL,
              merch_city VARCHAR(23) NULL,
              merch_state VARCHAR(10) NULL,
              acq_id VARCHAR(5) NULL,
              amt DECIMAL(10,2) NULL,
              status VARCHAR(1) NULL,
              xid INT NULL,
              process_ts DATETIME NULL,
              file_name VARCHAR(100) NULL,
              PRIMARY KEY (trans_id))
            COMMENT = 'Table is used to store transactions received via files, such as ACH.  ';
        """
        
        tables['activyt'] = """
            CREATE TABLE walgreens.activity (
              act_id INT NOT NULL AUTO_INCREMENT,
              act_type VARCHAR(5) NOT NULL,
              amount DECIMAL(10,2) NOT NULL,
              in_ts DATETIME NULL,
              source_id INT NULL,
              source_table VARCHAR(45) NULL,
              PRIMARY KEY (act_id))
            COMMENT = 'Used to store transactions against accounts';
        """
        
        for key, sql in tables.iteritems():
            print 'creating ', key, ' if it does not exist'
            self.db.execute(sql)

    def random_adjective(self):
        """
        Gets a random adjective from the adj array
        :return: string
        """
        result = ''
        while result == '':
            result = self.adj[randrange(0, len(self.adj)-1)].strip()
        return result

    def random_noun(self):
        """
        Gets a random noun from the noun array
        :return: string
        """
        result = ''
        while result == '':
            result = self.noun[randrange(0, len(self.noun)-1)].strip()
        return result

    def random_verb(self):
        """
        Gets a random verb from the verb array
        :return:
        """
        result = ''
        while result == '':
            result = self.verb[randrange(0, len(self.verb)-1)].strip()
        return result

    def random_addr_nbr(self):
        """
        Builds a random address number
        :return: string, 2 to 5 characters in length that is all digits from 1-9
        """
        cnt = randrange(2, 5)
        nbr = ''
        for i in range(0, cnt):
            nbr += str(randrange(1, 9))
        return nbr

    def street_name(self):
        """
        Builds a randomly named street address by combining a random adj and noun.
        :return: string
        """
        name = self.random_adjective().capitalize() + self.random_noun()
        return name

    def street_type(self):
        """
        Gets a random street type
        :return: string
        """
        types = ['Street', 'Lane', 'Avenue', 'Road', 'Circle', 'Bypass', 'Highway']
        return types[randrange(0, len(types)-1)]

    def random_street(self):
        """
        Builds a full street name, valid for an address.
        :return: string
        """
        return self.random_addr_nbr() + ' ' + self.street_name() + ' ' + self.street_type()

    def random_city(self):
        """
        Gets a random city
        :return: string
        """
        city = ''
        while not city:
            idx = randrange(0, len(self.city)-1)
            city = self.city[idx]
        return city

    def random_zip(self):
        """
        Builds a randomly generated 5 digit zip code (prob not a valid one).
        :return: string
        """
        nbr = ''
        for i in range(0, 5):
            nbr += str(randrange(0, 9))
        return nbr

    def random_first_name(self):
        """
        Gets a random first name.
        :return: string
        """
        first_name = ''
        while not first_name:
            idx = randrange(0, len(self.first_names)-1)
            first_name = self.first_names[idx].strip()
        return first_name

    def random_last_name(self):
        """
        Gets a random last name
        :return: string
        """
        last_name = ''
        while not last_name:
            idx = randrange(0, len(self.last_names)-1)
            last_name = self.last_names[idx].strip()
        return last_name

    def create_data(self):
        """
        Truncates the data tables and then loads them up with random data.
        :return: None
        """
        self.db.execute('truncate table ac_client')
        self.db.execute('truncate table ac_account')
        self.db.execute('truncate table ac_balance')
        self.db.execute('truncate table ac_card')

        # loop TOTAL_RECORD times and create dummy data.
        # Notice the weird crap in the values string on insert statements.
        # Thats a nice feature of mysql driver here.  That %(key)s names a key within a dictionary you
        # pass into the execute function and it puts that value in place of the %(key)s string.  Pretty cool.
        # Also, you need to know this for your next task :D
        for i in range(0, TOTAL_RECORDS):
            sql = """
                INSERT INTO ac_client (fname, lname, addr1, city, state, zip)
                VALUES (%(fname)s, %(lname)s, %(addr1)s, %(city)s, %(state)s, %(zip)s)
            """

            data = {
                'fname': self.random_first_name(),
                'lname': self.random_last_name(),
                'addr1': self.random_street(),
                'city': self.random_city(),
                'state': self.states[randrange(0, len(self.states)-1)],
                'zip': self.random_zip()
            }
            client_id = self.db.execute(sql, data, commit=True)


            bal_data = {
                'open_to_buy': float(str(randrange(20, 800)) + '.' + str(randrange(1, 99))),
                'cred_lim': 0
            }
            bal_sql = """
                INSERT INTO ac_balance (open_to_buy, cred_lim)
                VALUES (%(open_to_buy)s, %(cred_lim)s)
            """
            bal_id = self.db.execute(bal_sql, bal_data, commit=True)

            acct_data = {
                'bal_id': bal_id,
                'client_id': client_id,
                'status': 'N'
            }
            acct_sql = """
                INSERT INTO ac_account (bal_id, client_id, status)
                VALUES (%(bal_id)s, %(client_id)s, %(status)s)
            """
            xid = self.db.execute(acct_sql, acct_data, commit=True)

            # JAK - This dict contains a process that would be good to understand - list comprehension.
            # You see the card number built below.  The code in the square brackets is a list comprehension.
            # basically it says, in this case: for 12 time, create a string array element of a random
            # number between 1 and 9.  This functionality is fairly unique to python and is very common
            # to see.  what is happening is that you get an array of 12 digits that are joined together
            # using ''.join(array) to create a single string that is then combined with the '4217' string.
            card_data = {
                'xid': xid,
                'card_number': '4217' + ''.join([str(randrange(1, 9)) for n in xrange(12)]),
                'expiry_date': date(randrange(2018, 2020), randrange(1, 12), randrange(1, 28)),
                'card_status': 'N'
            }
            card_sql = """
                INSERT INTO ac_card (xid, card_number, expiry_date, card_status)
                VALUES (%(xid)s, %(card_number)s, %(expiry_date)s, %(card_status)s)
            """
            cad = self.db.execute(card_sql, card_data, commit=True)


if __name__ == '__main__':
    db = DbLoader()
    db.create_database()
    db.create_tables()
    db.create_data()

