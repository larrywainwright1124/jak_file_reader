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
