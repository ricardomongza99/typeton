from re import I
from typing import Dict

from src.compiler.stack_allocator.types import ValueType
from src.utils.display import make_table, TableOptions


class ClassVariable:
    def __init__(self, id_, offset):
        self.id_ = id_
        self.type_ = None
        self.offset = offset


class ClassTable:
    def __init__(self):
        self.classes: Dict[str, Class] = {}
        self.current_class: Class = None

    def add_class(self, id_):
        if id_ in self.classes:
            print("already registered")
            # TODO already exists
            return

        self.classes[id_] = Class(id_)
        self.current_class = self.classes[id_]

    def class_size(self, id_):
        if id_ not in self.classes:
            return None
        return self.classes[id_].size

    def get_class(self, id_):
        return self.classes[id_]

    def display(self):
        """ Displays symbol_table of functions tables """

        print(make_table("Class Directory", ["ID", "SIZE"],
                         map(lambda fun: [fun[1].id_, fun[1].size], self.classes.items())))

        for key in self.classes:
            print(key)
            val = self.classes[key]
            val.display()

    def end_class(self):
        self.current_class.size = len(self.current_class.variables)


class Class:
    def __init__(self, id_):
        self.current_variable = None
        self.id_ = id_
        self.size = 0
        self.offset = 0
        self.test = []
        self.variables: Dict[str, ClassVariable] = {}

    def add_variable(self, id_):
        if id_ in self.variables:
            # TODO already exists
            return
        self.test.append(2)

        self.variables[id_] = ClassVariable(id_, self.offset)
        self.current_variable = self.variables[id_]
        self.offset += 1

    def set_type(self, type_: ValueType):
        # if type_ is ValueType.VOID or type_ is ValueType.POINTER:
        #     # del self.variables[self._current_variable.id_]
        #     # self._current_variable = None
        #     # TODO error handling
        #     return

        self.current_variable.type_ = type_

    def display(self):
        print(len(self.test))
        for x in self.variables:
            print(x)
        print(make_table(self.id_ + ": Variables", ["ID", "TYPE", "OFFSET"],
                         map(lambda fun: [
                             fun[1].id_, fun[1].type_.value, fun[1].offset], self.variables.items()),
                         TableOptions(20, 20)))
