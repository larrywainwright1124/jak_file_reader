import argparse
from db import DB
from datetime import datetime
from decimal import Decimal


class LineParse:
    """
    Primary manager of line parsing functionality
    """

    def __init__(self, sections):
        """
        Constructor
        :param sections: dict of sections describing how to parse a string of text.
                        elements:
                            * from: starting position to read from
                            * to: position to read to
                            * name: name of element, can be anything but if its going into a table, consider
                                    using the column name.
                            * type: data type, currently str - string, int - integer, dec - decimal and
                                    date - datetime are supported.
                            * fn: defines a comma separated list of functions to call to modify the value:
                                    These are the only functions defined so far but more could be added easily
                                    lpad0 - strip zeros from the beginning of the value
                                    div100 - turn the value into an int and divide by 100.0
                            * fmt: if the type is a date, then a fmt must be defined as the code makes this
                                    assumption.  look up strptime in datetime for formats.  The format used
                                    below is %Y%m%d and means YYYYMMDD
                            * value: This is created in parse() and represents the content pulled from
                                    the section of the line for this definition.
        """
        self.line = ''
        self.sections = sections

    def parse(self, line):
        """
        Parse the line according to the rules defined in the sections setup.
            Grab the value from the string
            Strip spaces
            if fn has been defined, get the function names and call them on the value
            switch data type if needed
        :param line: String to parse
        :return: None
        """
        for item in self.sections:
            item['value'] = line[item['from']:item['to']].strip()
            fn = ''
            if 'fn' in item:
                fn = item['fn'].split(',')
            if fn:
                for func in fn:
                    mth = getattr(self, func)
                    item['value'] = mth(item['value'])

            if item['type'] == 'int':
                item['value'] = int(item['value'])
            elif item['type'] == 'dec':
                item['value'] = Decimal(item['value'])
            elif item['type'] == 'date':
                item['value'] = datetime.strptime(item['value'], item['fmt'])

    def lpad0(self, value):
        """
        Remove zeros from the beginning of the value
        :param value: Value to strip zeros from.
        :return: value with leading zeros stripped
        """
        return value.lstrip('0')

    def div100(self, value):
        """
        Take the value, convert it to an int and divide it by 100.0, turning it into a float.  The assumption
        is that we are operating on a pennies based value.
        :param value: string value to modify
        :return: Float
        """
        return int(value) / 100.0

    def get_item_by_index(self, index):
        """
        Find and return a section by it's index
        :param index: int - index into sections array
        :return: section dict from the sections array.
        """
        result = None
        try:
            result = self.sections[index]
        except:
            pass
        return result

    def get_item(self, name):
        """
        Find and return a section item by its name.
        :param name: Name of section to locate
        :return: section dict from the sections array
        """
        result = None
        for s in self.sections:
            if s['name'] == name:
                result = s
                break
        return result

    def value(self, name):
        """
        Find a section by its name and return its value.
        :param name: Name of section to locate
        :return: the value of the value element in the located section or None if not found.
        """
        item = self.get_item(name)
        if item:
            return item['value']

        return None

    def name_value_dict(self, exclude=None):
        """
        Return a name/value based dictionary containing the name element as the key and the value element
        as the key's value for each section that is not named within the exclude array.
        :param exclude: array of string based names to exclude from the returned results.
        :return: dict
        """
        d = {}
        for s in self.sections:
            if s['name'] not in exclude:
                d[s['name']] = s['value']
        return d


class Header(LineParse):
    """
    Child of LineParse used to define sections
    """
    def __init__(self):
        """
        Constructor - defines the sections and then calls parent constructor
        """
        sections = [
            {'from': 0, 'to': 6, 'type': 'int', 'fn': 'lpad0', 'name': 'record_count'},
            {'from': 6, 'to': 12, 'type': 'int', 'fn': 'lpad0', 'name': 'nbr_debits'},
            {'from': 12, 'to': 18, 'type': 'int', 'fn': 'lpad0', 'name': 'nbr_payments'},
            {'from': 18, 'to': 30, 'type': 'dec', 'fn': 'lpad0,div100', 'name': 'total_debits'},
            {'from': 30, 'to': 42, 'type': 'dec', 'fn': 'lpad0,div100', 'name': 'total_payments'}
        ]
        LineParse.__init__(self, sections)


class Record(LineParse):
    """
    Child of LineParse used to defined sections
    """
    def __init__(self):
        """
        Constructor - defines the sections and then calls parent constructor
        """
        sections = [
            {'from': 0, 'to': 6, 'type': 'int', 'fn': 'lpad0', 'name': 'index'},
            {'from': 6, 'to': 9, 'type': 'str', 'name': 'trans_type'},
            {'from': 9, 'to': 25, 'type': 'str', 'name': 'account_nbr'},
            {'from': 25, 'to': 33, 'type': 'date', 'fmt': '%Y%m%d', 'name': 'trans_date'},
            {'from': 33, 'to': 58, 'type': 'str', 'name': 'merch_name'},
            {'from': 58, 'to': 81, 'type': 'str', 'name': 'merch_city'},
            {'from': 81, 'to': 91, 'type': 'str', 'name': 'merch_state'},
            {'from': 91, 'to': 96, 'type': 'str', 'name': 'acq_id'},
            {'from': 96, 'to': 108, 'type': 'dec', 'fn': 'lpad0,div100', 'name': 'amt'}
        ]
        LineParse.__init__(self, sections)


class FileParser:
    """
    Handles the reading in of the file and storing the data into tp_trans
    """
    def __init__(self, dbname, file_name):
        """
        Constructor
        :param dbname: name of database to connect to
        :param file_name: Name of the file that will be parsed.
        """
        self.dbname = dbname
        self.file_name = file_name
        self.db = DB(self.dbname, 'root', 'root')

    def parse(self):
        """
        Parses the file and writes the transaction records into tp_trans.
        :return: None
        """
        head_parser = Header()
        records = []
        with file(self.file_name, 'r') as f:
            hdr = f.read(42)
            head_parser.parse(hdr)

            rec = f.read(108)
            while rec:
                r = Record()
                r.parse(rec)
                records.append(r)
                rec = f.read(108)

                nvp = r.name_value_dict(exclude=['index'])
                nvp['in_ts'] = datetime.now()
                nvp['status'] = 'N'
                nvp['file_name'] = self.file_name
                self.db.insert('tp_trans', nvp)


if __name__ == '__main__':
    """
    This is an example of how you start something up so that it can only run one time.  You will see this
    done frequently within an application.
    The argument parser is a very nice feature for working with command line arguments.  The functionality
    in use below is just barely representative of it's capabilities.
    """
    parser = argparse.ArgumentParser(usage=None, description="Parse data file into tp_trans")
    parser.add_argument('dbname', help="Name of the database to work with")
    parser.add_argument('file_name', help="Full path to the file to parse")

    args = parser.parse_args()

    fp = FileParser(args.dbname, args.file_name)
    fp.parse()
