from vars_table import VarsTable

# NOTE: `id` and `type` are reserved word in python, so
# we use the underscore at the end convention `id_` and `type_


class Function:
    def __init__(self, type_):
        self.type_ = type_
        self.vars_table = VarsTable()


class DirFunc:
    def __init__(self):
        self.functions = {}
        self.current_id = 'global'
        self.add('global')

    @property
    def current_func(self):
        return self.functions[self.current_id]

    def add(self, id_):
        """ Add Function to `functions` dictionary if not existent """
        if self.functions.get(id_) is None:
            self.current_id = id_
            self.functions[id_] = Function('Void')

    def set_type(self, type_):
        """ Sets current function type """
        self.current_func.type_ = type_

    def add_variable(self, id_):
        self.current_func.vars_table.add(id_)

    def display(self, show_var_tables=False):
        print("-" * 20)
        print("DIRECTORY FUNCTIONS")
        print("-" * 20)
        print('{:10} {:10}'.format('ID', 'TYPE'))
        print("-" * 20)
        for id_, function in self.functions.items():
            print('{:10} {:10}'.format(id_, function.type_))
        print("-" * 20)

        if show_var_tables:
            for id_, function in self.functions.items():
                print("\n\n")
                function.vars_table.display(id_)

