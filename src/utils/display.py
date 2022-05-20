from typing import List


class PrettyTable:
    def __init__(self, name="Unnamed Table", columns: List[str] = [], spacing=10, outline_len=20):
        self.name = name
        self.columns: List[str] = columns
        self.outline_len = outline_len
        self.raw = ''
        self.spacing = spacing
        self.max_row_len = 0
        self.table_rows = []

    def __add_row(self, content):
        self.raw += content + "\n"

    def __add_outline(self):
        self.__add_row("-" * self.max_row_len)

    def __add_title(self):
        self.__add_outline()
        self.__add_row(self.name)
        self.__add_outline()

    def __add_header(self):
        columns = ('{:<' + str(self.spacing) + '} ') * len(self.columns)
        columns = columns.format(*self.columns)
        self.max_row_len = max(self.max_row_len, len(columns))
        self.__add_title()
        self.__add_row(columns)
        self.__add_outline()

    def add_table_row(self, values: []):
        spacing = ('{:<' + str(self.spacing) + '} ') * len(values)
        values = map(lambda val: val if val is not None else "____", values)
        row = spacing.format(*values)
        self.table_rows.append(row)

    def add_table_rows(self, rows=[]):
        for row in rows:
            self.add_table_row(row)

    def __add_rows(self):
        for row in self.table_rows:
            self.__add_row(row)

    def __add_newline(self):
        self.__add_row("")

    def __add_footer(self):
        self.__add_outline()

    def __build_table(self):
        self.raw = ''
        self.__add_header()
        self.__add_rows()
        self.__add_footer()

    def get_table(self):
        self.__build_table()
        return self.raw

    def display(self):
        self.__build_table()
        print(self.raw)


class TableOptions:
    def __init__(self, row_spacing, outline_len):
        self.row_spacing = row_spacing
        self.outline_len = outline_len


def make_table(name, columns, rows, options=TableOptions(10, 20)):
    table = PrettyTable(name, columns, options.row_spacing, options.outline_len)
    table.add_table_rows(rows)
    return table.get_table()
