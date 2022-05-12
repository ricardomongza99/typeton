# NOTE: `id` and `type` are reserved word in python, so
# we use the underscore at the end convention `id_` and `type_

class Variable:
    def __init__(self, type_, dir_):
        self.type_ = type_
        self.dir_ = dir_


class VarsTable:
    def __init__(self):
        self.vars = {}
        self.current_id = None

    @property
    def current_var(self):
        return self.vars[self.current_id]

    def add(self, id_):
        """ Add Variable to `variables` dictionary if not existent """
        if self.vars.get(id_) is None:
            # TODO: Default type should not be Int
            # TODO: Replace 1000 with correct memory directory
            self.current_id = id_
            self.vars[id_] = Variable(None, 1000)

    def set_type(self, type_):
        self.current_var.type_ = type_

    def display(self, id_):
        print("-" * 30)
        print(f"{id_} VARS TABLE")
        print("-" * 30)
        print('{:10} {:10} {:10}'.format('ID', 'TYPE', 'DIR'))
        print("-" * 30)
        for id_, var in self.vars.items():
            # Unwrap optional. If var type is None use 'Undefined'
            type_ = 'Undefined' if var.type_ is None else var.type_

            print('{:10} {:10} {:10}'.format(id_, type_, str(var.dir_)))
        print("-" * 30)