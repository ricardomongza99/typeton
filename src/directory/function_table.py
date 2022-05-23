from typing import List, Dict

from .function import Function
from ..parser.errors import CompilerError
from ..singleton.debug import Debug
from ..utils.display import make_table, TableOptions
from ..virtual.compilation import Scheduler
from ..virtual.helpers import Layers
from ..virtual.types import ValueType
from ..virtual_machine.types import FunctionData


class FunctionTable:
    """ A directory of functions """

    def __init__(self):
        self.functions = {}
        self.function_data_table: Dict[str, FunctionData] = {}
        self.function_stack: List[Function] = []
        self.add("global", 0)

    def current_function(self) -> Function:
        return self.function_stack[len(self.function_stack) - 1]

    def add(self, id_, quad_start: int, is_void):
        """ Add Func to `funcs` dictionary if not existent """
        if self.functions.get(id_) is None:
            reference = Function(id_=id_)
            reference.pending_type = not is_void
            reference.type_ = ValueType.VOID
            self.functions[id_] = reference
            self.function_stack.append(reference)

            # persistent for vm
            self.function_data_table[id_] = FunctionData(id_, quad_start)
            self.function_data_table[id_].type_ = ValueType.VOID
            return

        return CompilerError(f'Function {id_} redeclared')

    def add_variable(self, id_, is_param):
        """ Add Var to the current function's vars table """
        self.current_function().vars_table.add(id_, is_param)

    def set_function_type(self, type_):
        self.current_function().set_type(type_)

        self.function_data().type_ = ValueType(type_)

    def set_param_type(self, type_, memory: Scheduler):
        layer = Layers.GLOBAL if self.current_function().id_ == "global" else Layers.LOCAL
        self.function_data_table[self.current_function().id_].add_variable_size(ValueType(type_))
        return self.current_function().vars_table.set_type(type_, layer, memory)

    def function_data(self):
        return self.function_data_table[self.current_function().id_]

    def set_variable_type(self, type_, memory: Scheduler):
        layer = Layers.GLOBAL if self.current_function().id_ == "global" else Layers.LOCAL
        self.function_data().add_variable_size(ValueType(type_))
        id_ = self.current_function().vars_table.set_type(type_, layer, memory)

        if self.current_function().is_pending_type():
            return self.set_function_type(type_)

        is_param = self.current_function().vars_table.current_variable.is_param
        if is_param:
            return self.__add_parameter_signature(type_)

        return id_

    def __add_parameter_signature(self, type_):
        self.function_data_table[self.current_function().id_].parameter_signature.append(ValueType(type_))

    def display(self, debug=False):
        """ Displays directory of functions tables """

        print(make_table("Function Directory", ["ID", "TYPE"],
                         map(lambda fun: [fun[0], fun[1].type_.value], self.functions.items())))

        print(make_table("VM Directory Data",
                         [
                             "Id",
                             "Type",
                             "Quad Start",
                             "Param Signature", "Int Count", "Float Count", "Bool Count", "String Count"],
                         map(
                             lambda fun: [
                                 fun[0],
                                 fun[1].type_.value,
                                 fun[1].start_quad,
                                 fun[1].print_signature(),
                                 fun[1].size_data.int_count,
                                 fun[1].size_data.float_count,
                                 fun[1].size_data.bool_count,
                                 fun[1].size_data.string_count,
                             ],
                             self.function_data_table.items()), TableOptions(25, 50)))

        if debug:
            for id_, func in self.functions.items():
                print(func.vars_table.display(id_))

    def end_function(self, memory: Scheduler):
        """ Releases Function From Directory and Virtual Memory"""

        error = self.__validate_return()

        if len(self.function_stack) > 1:
            function: Function = self.function_stack.pop()

            for key in function.vars_table.variables:
                address = function.vars_table.variables[key].address_
                memory.release_address(address)

        if error is not None:
            return error

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

    def set_return(self):
        self.current_function().has_return = True

    def __validate_return(self):
        if not self.current_function().valid_function():
            void_error = f'Void function should not return a value'
            type_error = f'Function should return {self.current_function().type_.value}'
            return CompilerError(
                void_error if self.current_function().type_ is ValueType.VOID else type_error,
                trace=self.current_trace()
            )
        return None
