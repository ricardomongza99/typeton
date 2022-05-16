# NOTE: `type` is a reserved words in python, so
# we use the underscore at the end convention `type_`
from src.virtual.types import ValueType


class Variable:
    def __init__(self, type_: ValueType or None, address):
        self.type_ = type_
        self.address_ = address
