# NOTE: `type` is a reserved words in python, so
# we use the underscore at the end convention `type_`

class Variable:
    def __init__(self, type_, address):
        self.type_ = type_
        self.address_ = address
