import mysql.connector
from mysql.connector import errorcode


class DB:
    """
    Interface to ease querying against mysql
    """

    def __init__(self, database, user, pwd):
        """
        Constructor - stores the connection info and tries to create a connection.
        :param database:
        :param user:
        :param pwd:
        """
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
        """
        Destructor, destroy the connection
        :return: None
        """
        try:
            self.conn.close()
        except:
            pass

    def connect(self, database, user, pwd, host='localhost'):
        """
        Connects to mysql and the the referenced database.
        :param database: name of database to connect to
        :param user: user to log in as
        :param pwd: password of user
        :param host: host name - default is localhost
        :return: None
        """
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
        """
        switches to different database.
        :param db_name: name of database to switch to
        :return: None
        """
        try:
            self.conn.database = db_name
            self.database = db_name
        except mysql.connector.Error as err:
            print err.msg

    def get_cursor(self):
        """
        Retrieves a cursor from the connection.  By default it causes the cursor to return data as a
        dictionary.  This is not always desirable, for instance, when using a stored procedure.  In those
        cases, it may be more desirable to get the cursor yourself or use the proc method.
        :return: cursor
        """
        cursor = None
        try:
            cursor = self.conn.cursor(dictionary=True)
        except mysql.connector.Error as err:
            print err.msg

        return cursor

    def execute(self, sql, params=None, commit=False):
        """
        Executes a sql statement
        :param sql: sql statement
        :param params: params in the query in the form of a dictionary
        :param commit: True/False, whether to commit
        :return: None or auto incremented id if an insert statement
        """
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
        """
        Intended to be used internally by this class.  Creates a cursor, executes the query
        and returns the cursor for further operations, such as retrieving results.
        :param sql: sql query
        :param params: params in dictionary form
        :return: cursor
        """
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
        """
        Returns one record result from the query
        :param sql: sql query statement
        :param params: dictionary of params
        :return: dictionary
        """
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
        """
        Retrieves all records of the result of the query
        :param sql: sql query statement
        :param params: dictionary of params
        :return: array of dictionary based records.
        """
        cursor = self.execute_ret_cursor(sql, params)
        data = []
        if cursor:
            try:
                data = cursor.fetchall()
            except mysql.connector.Error as err:
                print err.msg
        return data

    def fetch_col(self, col_name, sql, params=None):
        """
        Retrieves a single column from the first record of the result set.
        :param col_name: column name to retrieve data for
        :param sql: sql query
        :param params: dictionary of params
        :return: value of the named column requested in col_name.
        """
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

    def insert(self, tbl_name, key_vals):
        vals = {}
        ins_cols = ', '.join([key for key in key_vals])
        ins_vals = ', '.join(['%(' + key + ')s' for key in key_vals])
        insert_sql = "insert into {tbl} ({cols}) values ({vals})".format(tbl=tbl_name, cols=ins_cols,
                                                                         vals=ins_vals)
        id = self.execute(insert_sql, key_vals, True)
        return id
