from typing import Dict

from .function import Function
from ..allocator.allocator import Allocator
from ..allocator.helpers import Layers
from ..allocator.types import ValueType
from ..parser.errors import CompilerError
from ..utils.debug import Debug
from ..utils.display import make_table, TableOptions
from ..virtual_machine.types import FunctionData


class FunctionTable:
    """ A directory of functions """

    def __init__(self):
        self.functions = {}
        self.function_data_table: Dict[str, FunctionData] = {}
        self.current_function: Function = None

        # We need this for global variable search
        self.add("global", 0)
        self.current_function.set_type("Void")

    def add(self, id_, quad_start: int):
        """ Add Func to `funcs` dictionary if not existent """
        if self.functions.get(id_) is None:
            reference = Function(id_=id_)
            self.functions[id_] = reference
            self.current_function = reference

            # persistent for vm
            self.function_data_table[id_] = FunctionData(id_, quad_start)
            self.function_data_table[id_].type_ = ValueType.VOID
            return

        return CompilerError(f'Function {id_} redeclared')

    def add_variable(self, id_, is_param):
        """ Add Var to the current function's vars table """
        self.current_function.add_variable(id_, is_param)

    def set_function_type(self, type_):
        self.current_function.set_type(type_)
        self.function_data().type_ = ValueType(type_)

    def set_param_type(self, type_, memory: Allocator):

        self.function_data().add_variable_size(ValueType(type_))
        return self.current_function.set_variable_type(type_, Layers.LOCAL, memory)

    def function_data(self):
        return self.function_data_table[self.current_function.id_]

    def set_variable_type(self, type_, memory: Allocator):
        layer = Layers.GLOBAL if self.current_function.id_ == "global" else Layers.LOCAL
        self.function_data().add_variable_size(ValueType(type_))
        id_ = self.current_function.set_variable_type(type_, layer, memory)

        if self.current_function.is_pending_type():
            return self.set_function_type(type_)

        # TODO encapsulate methods in function to prevent so many dot operations
        is_param = self.current_function.current_variable.is_param
        if is_param:
            return self.__add_parameter_signature(type_)

        return id_

    def __add_parameter_signature(self, type_):
        self.function_data_table[self.current_function.id_].parameter_signature.append(ValueType(type_))

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
                func.display_variables(id_)

        # print(Debug.map()[3000])

    def end_function(self, memory: Allocator):
        """ Releases Function From Directory and Virtual Memory"""
        error = self.__validate_return()

        for key in self.current_function.variables:
            address = self.current_function.variables[key].address_
            memory.release_address(address)

        if error is not None:
            return error

    def current_trace(self):
        return self.current_function.id_

    def find(self, id_):
        variable_table = self.current_function.variables
        if variable_table.get(id_) is not None:
            variable = variable_table[id_]
            return variable.address_, variable.type_

        variable_table = self.functions["global"]
        if variable_table.get(id_) is not None:
            variable = variable_table[id_]
            return variable.address_, variable.type_

        return None, None

    def set_return(self):
        self.current_function.has_return = True

    def __validate_return(self):
        if not self.current_function.valid_function():
            void_error = f'Void function should not return a value'
            type_error = f'Function should return {self.current_function.type_.value}'
            return CompilerError(
                void_error if self.current_function.type_ is ValueType.VOID else type_error,
                trace=self.current_trace()
            )
        return None
