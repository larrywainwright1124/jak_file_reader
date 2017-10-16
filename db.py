import mysql.connector
from mysql.connector import errorcode


class DB:

    def __init__(self, database, user, pwd):
        self.database = database
        self.user = user
        self.pwd = pwd

        self.conn = None
        self.connect(database=database, user=user, pwd=pwd)

        try:
            self.cursor = self.conn.cursor()
        except:
            pass

    def __del__(self):
        try:
            self.conn.close()
        except:
            pass

    def connect(self, database, user, pwd, host='localhost'):
        self.database = database
        self.user = user
        self.pwd = pwd

        try:
            self.conn = mysql.connector.connect(user=user, password=pwd, host=host, database=database)
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print "something is wrong with your user/pass"
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print "Database does not exist"
            else:
                print err

    def select_database(self, db_name):
        try:
            self.conn.database = db_name
            self.database = db_name
        except mysql.connector.Error as err:
            print err.msg

    def get_cursor(self):
        cursor = None
        try:
            cursor = self.conn.cursor(dictionary=True)
        except mysql.connector.Error as err:
            print err.msg

        return cursor

    def execute(self, sql, params=None, commit=False):
        id = None
        cursor = self.get_cursor()
        if not cursor:
            return

        try:
            if params:
                cursor.execute(sql, params)
            else:
                cursor.execute(sql)

            if commit:
                self.conn.commit()
            if 'insert' in sql.strip().lower()[0:6]:
                id = cursor.lastrowid

        except mysql.connector.Error as err:
            print err.msg

        return id

    def execute_ret_cursor(self, sql, params=None):
        cursor = self.get_cursor()
        if not cursor:
            return None

        try:
            if params:
                cursor.execute(sql, params)
            else:
                cursor.execute(sql)
        except mysql.connector.Error as err:
            print err.msg
            return None

        return cursor

    def fetch_one(self, sql, params=None):
        cursor = self.execute_ret_cursor(sql, params)
        row = {}
        if cursor:
            try:
                data = cursor.fetchall()
                if cursor.rowcount > 0:
                    row = data[0]
            except mysql.connector.Error as err:
                print err.msg

        return row

    def fetch_all(self, sql, params=None):
        cursor = self.execute_ret_cursor(sql, params)
        data = []
        if cursor:
            try:
                data = cursor.fetchall()
            except mysql.connector.Error as err:
                print err.msg
        return data

    def fetch_col(self, col_name, sql, params=None):
        cursor = self.execute_ret_cursor(sql, params)
        result = ''
        if cursor:
            try:
                data = cursor.fetchall()
                if cursor.rowcount > 0:
                    row = data[0]
                    result = row[col_name]
            except mysql.connector.Error as err:
                print err.msg
        return result

    def proc(self, proc_name, args):
        """
        This method kind of sucks.  It requires the arguments to be in a tuple which, in this case,
        would be the parameters to the procedure wrapped in (), so if u were calling adjustment:
        (1, 55.67, 1, 'tp_trans', '--')
        You get back that same list with the out parameter changed would would be referenced in the returned
        result like so:
        result = db.proc('adjustment', (1, 55.67, 1, 'tp_trans', '--')
        print result[4] => '00' or '01' or '02'
        result[4] is the last value in the tuple and was passed in as '--'.  Tuples are referenced like arrays
        with the first position being 0.
        :param proc_name: Name of the procedure to call
        :param args: Tuple of arguments in the same order as defined in the stored procedure.
        :return: Tuple with same arguments but any that were defined as out will have a different value.
        """
        cursor = self.conn.cursor()
        result_args = None
        if cursor:
            try:
                result_args = cursor.callproc(proc_name, args)
            except mysql.connector.Error as err:
                print err.msg

        return result_args
