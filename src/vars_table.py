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
            self.variables[id_] = Variable(type_, value)