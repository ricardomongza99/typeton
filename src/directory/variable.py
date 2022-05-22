# NOTE: `type` is a reserved words in python, so
# we use the underscore at the end convention `type_`


class Variable:
    def __init__(self, is_param=False):
        self.type_ = None
        self.address_ = None
        self.isReturned = None
        self.is_param = is_param
