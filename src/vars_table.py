# NOTE: `id` and `type` are reserved word in python, so
# we use the underscore at the end convention `id_` and `type_

class Variable:
    def __init__(self, type_, dir_):
        self.type_ = type_
        self.dir_ = dir_


class VarsTable:
    def __init__(self):
        self.variables = {}

    def add(self, id_):
        """ Add Variable to `variables` dictionary if not existent """
        if self.variables.get(id_) is None:
            # TODO: Default type should not be Int
            # TODO: Replace 1000 with correct memory directory
            self.variables[id_] = Variable('Int', 1000)

    def display(self, id_):
        print("-" * 30)
        print(f"{id_} VARS TABLE")
        print("-" * 30)
        print('{:10} {:10} {:10}'.format('ID', 'TYPE', 'DIR'))
        print("-" * 30)
        for id_, variable in self.variables.items():
            print('{:10} {:10} {:10}'.format(id_, variable.type_, str(variable.dir_)))
        print("-" * 30)