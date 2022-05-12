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
        self.add('global', 'Void')

    def add(self, id_, type_):
        """ Add Function to `functions` dictionary if not existent """
        if self.functions.get(id_) is None:
            self.current_id = id_
            self.functions[id_] = Function(type_)

    def set_type(self, type_):
        self.functions[self.current_id].type_ = type_

    def display(self):
        print("-" * 20)
        print("DIRECTORY FUNCTIONS")
        print("-" * 20)
        print('{:10} {:10}'.format('ID', 'TYPE'))
        print("-" * 20)
        for id_, function in self.functions.items():
            print('{:10} {:10}'.format(id_, function.type_))
        print("-" * 20)
