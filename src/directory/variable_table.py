from .variable import Variable


class VariableTable:
    def __init__(self):
        self.variables = {}
        self.current_id = None

    @property
    def current_variable(self):
        return self.variables[self.current_id]

    def add(self, id_):
        """ Add Variable to `variables` dictionary if not existent """
        if self.variables.get(id_) is None:
            # TODO: Replace 1000 with correct memory directory
            self.current_id = id_
            self.variables[id_] = Variable(None, 1000)

    def set_type(self, type_):
        """ Sets current var type """
        self.current_variable.type_ = type_

    def display(self, id_):
        print("-" * 30)
        print(f"{id_} VARS TABLE")
        print("-" * 30)
        print('{:10} {:10} {:10}'.format('ID', 'TYPE', 'DIR'))
        print("-" * 30)
        for id_, var in self.variables.items():
            # Unwrap optional. If var type is None use 'Undefined'
            type_ = 'Undefined' if var.type_ is None else var.type_

            print('{:10} {:10} {:10}'.format(id_, type_, str(var.address_)))
        print("-" * 30)