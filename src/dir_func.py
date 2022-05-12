from vars_table import VarsTable

# NOTE: `id` and `type` are reserved words in python, so
# we use the underscore at the end convention `id_` and `type_


class Func:
    def __init__(self, type_):
        self.type_ = type_
        self.vars_table = VarsTable()


class DirFunc:
    def __init__(self):
        self.funcs = {}
        self.current_id = 'global'
        self.add('global')
        self.is_func = True

    @property
    def current_func(self):
        return self.funcs[self.current_id]

    def add(self, id_):
        """ Add Func to `funcs` dictionary if not existent """
        if self.funcs.get(id_) is None:
            self.current_id = id_
            self.funcs[id_] = Func('Void')

    def add_var(self, id_):
        """ Add Var to the current function's vars table """
        self.current_func.vars_table.add(id_)

    def will_set_type(self, type_operator):
        """ Prepares for assigning type. Sets `is_func` to true if operator is function related -> """
        self.is_func = type_operator == '->'

    def set_type(self, type_):
        """ Sets corresponding type either to function or to variable"""
        if self.is_func:
            self.current_func.type_ = type_
        else:
            self.current_func.vars_table.set_type(type_)

    def display(self, debug=False):
        print("-" * 20)
        print("DIRECTORY FUNCTIONS")
        print("-" * 20)
        print('{:10} {:10}'.format('ID', 'TYPE'))
        print("-" * 20)
        for id_, func in self.funcs.items():
            print('{:10} {:10}'.format(id_, func.type_))
        print("-" * 20)
        print()
        if debug:
            for id_, func in self.funcs.items():
                func.vars_table.display(id_)
                print()

