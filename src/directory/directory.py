from .function import Function
from ..parser.errors import CompilerError
from ..virtual.compilation import Scheduler
from ..virtual.helpers import Layers
from ..virtual.types import ValueType


class Directory:
    """ A directory of functions """

    def __init__(self):
        self.functions = {}
        self.function_stack: [Function] = []
        self.add("global")
        self.is_function = True

    def current_function(self) -> Function:
        return self.function_stack[len(self.function_stack) - 1]

    def add(self, id_):
        """ Add Func to `funcs` dictionary if not existent """
        if self.functions.get(id_) is None:
            reference = Function(id_=id_, type_pending=True)
            self.functions[id_] = reference
            self.function_stack.append(reference)

    def add_variable(self, id_):
        """ Add Var to the current function's vars table """
        self.current_function().vars_table.add(id_)

    def will_set_type(self, type_operator):
        """ Prepares for assigning type. Sets `is_func` to true if operator is function related -> """
        self.current_function().type_pending = type_operator == '->'

    def set_type(self, type_, memory: Scheduler):
        layer = Layers.GLOBAL if self.current_function().id_ == "global" else Layers.LOCAL
        """ Sets corresponding type either to function or to variable"""
        if self.current_function().type_pending:
            self.current_function().set_type(type_)
        else:
            self.current_function().vars_table.set_type(type_, layer, memory)

    def display(self, debug=False):
        """ Displays directory of functions tables """
        print("-" * 20)
        print("DIRECTORY FUNCTIONS")
        print("-" * 20)
        print('{:10} {:10}'.format('ID', 'TYPE'))
        print("-" * 20)
        for id_, func in self.functions.items():
            print('{:10} {:10}'.format(id_, func.type_.value))
        print("-" * 20)
        print()
        if debug:
            for id_, func in self.functions.items():
                func.vars_table.display(id_)
                print()

    def end_function(self, memory: Scheduler):
        """ Releases Function From Directory and Virtual Memory"""
        if len(self.function_stack) > 1:
            function: Function = self.function_stack.pop()
            if function.is_valid():
                return CompilerError("Expected return for function with return type of ", function.type_.value)

            for key in function.vars_table.variables:
                address = function.vars_table.variables[key].address_
                memory.release_address(address)
