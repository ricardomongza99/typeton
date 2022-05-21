from .function import Function
from ..parser.errors import CompilerError
from ..singleton.debug import Debug
from ..utils.display import make_table
from ..virtual.compilation import Scheduler
from ..virtual.helpers import Layers


class FunctionTable:
    """ A directory of functions """

    def __init__(self):
        self.functions = {}
        self.function_stack: [Function] = []
        self.add("global")

    def current_function(self) -> Function:
        return self.function_stack[len(self.function_stack) - 1]

    def add(self, id_):
        """ Add Func to `funcs` dictionary if not existent """
        if self.functions.get(id_) is None:
            reference = Function(id_=id_)
            self.functions[id_] = reference
            self.function_stack.append(reference)
            return

        Debug.add_error(CompilerError(f'Function "{id_}" redeclared'))

    def add_variable(self, id_):
        """ Add Var to the current function's vars table """
        self.current_function().vars_table.add(id_)

    def set_function_type(self, type_):
        self.current_function().set_type(type_)

    def set_variable_type(self, type_, memory: Scheduler):
        layer = Layers.GLOBAL if self.current_function().id_ == "global" else Layers.LOCAL
        return self.current_function().vars_table.set_type(type_, layer, memory)

    def display(self, debug=False):
        """ Displays directory of functions tables """

        print(make_table("Function Directory", ["ID", "TYPE"],
                         map(lambda fun: [fun[0], fun[1].type_.value], self.functions.items())))

        if debug:
            for id_, func in self.functions.items():
                print(func.vars_table.display(id_))

    def end_function(self, memory: Scheduler):
        """ Releases Function From Directory and Virtual Memory"""
        if len(self.function_stack) > 1:
            function: Function = self.function_stack.pop()

            for key in function.vars_table.variables:
                address = function.vars_table.variables[key].address_
                memory.release_address(address)

    def current_trace(self):
        stack_copy = self.function_stack[:]
        stack_copy.reverse()
        trace = ""
        while len(stack_copy) > 0:
            function = stack_copy.pop()
            if len(stack_copy) == 0:
                trace += f'{function.id_}'
            else:
                trace += f'{function.id_}.'
        return trace

    def find(self, id_):
        stack_copy = self.function_stack[:]

        while len(stack_copy) > 0:  # go from local to global
            function = stack_copy.pop()
            variable_table = function.vars_table.variables
            if variable_table.get(id_) is not None:
                # segment = Layers.GLOBAL if function.id_ == 'global' else Layers.LOCAL
                variable = variable_table[id_]
                return variable.address_, variable.type_

        return None, None
