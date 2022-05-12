from vars_table import VarsTable

# NOTE: `id` and `type` are reserved word in python, so
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

    @property
    def current_func(self):
        return self.funcs[self.current_id]

    def add(self, id_):
        """ Add Func to `funcs` dictionary if not existent """
        if self.funcs.get(id_) is None:
            self.current_id = id_
            self.funcs[id_] = Func('Void')

    def set_type(self, type_):
        """ Sets current Func type """
        self.current_func.type_ = type_

    def add_var(self, id_):
        self.current_func.vars_table.add(id_)

    def set_var_type(self, type_):
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

