from audioop import add
from enum import Enum
from typing import Dict

import jsonpickle

from src.compiler.errors import CompilerError, CompilerEvent
from src.compiler.stack_allocator.helpers import Layers
from src.compiler.stack_allocator.index import StackAllocator
from src.compiler.stack_allocator.types import ValueType
from src.compiler.symbol_table.class_table import ClassTable
from src.compiler.symbol_table.function_table.variable_table.variable import Variable
from src.utils.display import make_table, TableOptions
from src.utils.observer import Subscriber, Event, Publisher
from src.virtual_machine.types import FunctionData
from .function import Function
from ...code_generator.type import FunctionTableEvents


class TypeContext(Enum):
    FUNCTION = 0
    PARAM = 1
    VARIABLE = 2


PRIMITIVE_TYPES = {ValueType.INT.value, ValueType.FLOAT.value,
                   ValueType.STRING.value, ValueType.BOOL.value, ValueType.POINTER.value}


class FunctionTable(Publisher, Subscriber):
    """ A symbol_table of functions """

    def __init__(self, class_table: ClassTable):
        super().__init__()
        self.functions = {}
        # keep track of them so we don't add repeat numbers to function size
        self.temporal_hash: Dict[int, Variable] = {}
        self.local_hash: Dict[int, Variable] = {}
        self.global_hash: Dict[int, Variable] = {}

        self.should_delete_temp = []
        self.class_table = class_table
        self.function_data_table: Dict[str, FunctionData] = {}

        self.current_function: Function = None

        self.parameter_count = 0

        # We need this for global variable search
        self.add("global", 0)
        self.current_function.set_type("Void")

    @property
    def _type_context(self) -> TypeContext:
        if self.current_function.is_pending_type():
            variable = self.current_function.current_variable
            if variable is None:
                return
            if variable.is_param and variable.type_ is None:
                return TypeContext.PARAM
            else:
                return TypeContext.FUNCTION
        else:
            return TypeContext.VARIABLE

    def handle_event(self, event: Event):
        """Receive all subscribed events here"""
        from src.compiler.code_generator.expression import ExpressionActions
        from src.compiler.code_generator.array import ArrayEvents

        if event.type_ is FunctionTableEvents.ADD_TEMP or event.type_ is ArrayEvents.ADD_TEMP:
            type_, address, class_id = event.payload
            self.__handle_add_temporal(type_, address, class_id)
        elif event.type_ is CompilerEvent.RELEASE_FUNCTION:
            self.end_function()

    def __handle_add_temporal(self, type_, address, class_id=None):
        if address in self.temporal_hash:
            return

        self.function_data().add_variable_size(ValueType(type_), Layers.TEMPORARY)
        var = Variable(None)
        var.address_ = address
        var.type_ = type
        var.class_id = class_id
        self.temporal_hash[address] = var

    def get_variable_by_address(self, address):
        """ Returns variable by address """
        if self.temporal_hash.get(address) is not None:
            return self.temporal_hash[address]

        if self.local_hash.get(address) is not None:
            return self.local_hash[address]

        if self.global_hash.get(address) is not None:
            return self.global_hash[address]

        self.broadcast(Event(CompilerEvent.STOP_COMPILE,
                       CompilerError(f'Variable with address {address} not found')))

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

        error = CompilerError(f'Function {id_} redeclared')
        self.broadcast(Event(CompilerEvent.STOP_COMPILE, error))

    def verify_function_exists(self, id_):
        if self.functions.get(id_) is None:
            self.broadcast(Event(
                CompilerEvent.STOP_COMPILE,
                CompilerError(f'Invalid Function Call: Function with name {id_} does not exist')))
        self.current_function_call_id_ = id_

    def generate_are_memory(self):
        self.broadcast(Event(CompilerEvent.GENERATE_ARE,
                       self.current_function_call_id_))
        # start counting param signature
        self.parameter_count = 0

    def add_variable(self, id_, is_param):
        """ Add Var to the current function's vars table """

        var = self.current_function.add_variable(id_, is_param)
        if self.current_function.id_ == "global":
            self.global_hash[id_] = var
            return
        self.local_hash[var.address_] = var

    def end_class(self):
        print('')

    def add_dimension(self, size):
        """ Adds dimension to current array """
        self.current_function.add_dimension(size)

    def allocate_dimensions(self, memory: StackAllocator, constant_table):
        """ Allocates spaces for array (Moves pointer x spaces) """
        layer = Layers.GLOBAL if self.current_function.id_ == 'global' else Layers.LOCAL
        return self.current_function.allocate_dimensions(layer, memory, constant_table)

    def set_type(self, type_, memory: StackAllocator):
        """ Sets type for function, parameter or variable """
        layer = Layers.GLOBAL if self.current_function.id_ == "global" else Layers.LOCAL

        if self._type_context == TypeContext.FUNCTION:
            self._set_function_type(type_)
        elif self._type_context == TypeContext.PARAM:
            self._set_param_type(type_, layer, memory)
        elif self._type_context == TypeContext.VARIABLE:
            id_ = self._set_variable_type(type_, layer, memory)
            return id_

    def _set_function_type(self, type_):
        self.current_function.set_type(type_)
        self.function_data().type_ = ValueType(type_)

    def _set_param_type(self, type_, layer, memory: StackAllocator):
        self.current_function.set_variable_type(type_, layer, memory, None)
        self.function_data().add_variable_size(ValueType(type_), layer)
        self.__add_parameter_signature(type_)

    def _set_variable_type(self, type_, layer, memory: StackAllocator):
        # check if parameter type_ first character is capitalized
        # its a class
        if type_[0].isupper() and type_ not in PRIMITIVE_TYPES:
            class_size = self.class_table.class_size(type_)
            if class_size is None:
                self.broadcast(
                    Event(CompilerEvent.STOP_COMPILE,
                          CompilerError(f'Class {type_} not found')))

            self.function_data().add_variable_size(ValueType.POINTER, layer)
            self.current_function.set_variable_type(
                ValueType.POINTER, layer, memory, type_)
            return

        self.function_data().add_variable_size(ValueType(type_), layer)
        id_ = self.current_function.set_variable_type(
            type_, layer, memory, None)
        return id_

    def function_data(self):
        return self.function_data_table[self.current_function.id_]

    def __add_parameter_signature(self, type_):
        self.function_data_table[self.current_function.id_].parameter_signature.append(
            ValueType(type_))

    def display(self, debug=False):
        """ Displays symbol_table of functions tables """

        print(make_table("Function Directory", ["ID", "TYPE"],
                         map(lambda fun: [fun[0], fun[1].type_.value], self.functions.items())))

        # TODO refactor size data lambda
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
                                 fun[1].size_data.get_data(
                                     ValueType.INT).total,
                                 fun[1].size_data.get_data(
                                     ValueType.FLOAT).total,
                                 fun[1].size_data.get_data(
                                     ValueType.BOOL).total,
                                 fun[1].size_data.get_data(
                                     ValueType.STRING).total,
                             ],
                             self.function_data_table.items()), TableOptions(25, 50)))

        if debug:
            for id_, func in self.functions.items():
                func.display_variables(id_)

    def end_function(self):
        """ Releases Function From Directory and Virtual Memory"""
        self.__validate_return()

        print("deleting", self.current_function.id_)

        # tell quad generator to generate end_func quad
        self.broadcast(Event(CompilerEvent.GEN_END_FUNC, None))

        delete_list = []

        for key in self.current_function.variables:
            delete_list.append(self.current_function.variables[key].address_)

        for key in self.temporal_hash:
            var = self.temporal_hash[key]
            delete_list.append(var.address_)

        self.broadcast(Event(CompilerEvent.FREE_MEMORY, None))
        self.temporal_hash = {}

    def current_trace(self):
        return self.current_function.id_

    def get_variable(self, id_):
        # Try to find local first
        variable_table = self.current_function.variables
        if variable_table.get(id_) is not None:
            return variable_table[id_]

        # Okay, maybe its global
        variable_table = self.functions["global"].variables
        if variable_table.get(id_) is not None:
            return variable_table[id_]

        print(f'Variable {id_} not found')

        # Could not find
        self.broadcast(Event(CompilerEvent.STOP_COMPILE,
                       CompilerError(f'variable {id_} is undefined')))

    def get_id(self, address):
        # Try to find local first
        variable_table = self.current_function.vars_table
        variable = variable_table.get_from_address(address)
        if variable is not None:
            return variable

        # Okay, maybe its global
        variable_table = self.functions["global"].vars_table
        variable = variable_table.get_from_address(address)
        if variable is not None:
            return variable

        if address in self.temporal_hash:
            return self.temporal_hash[address]

        # Could not find
        self.broadcast(Event(CompilerEvent.STOP_COMPILE, CompilerError(
            f'variable at address {address} is undefined')))

    def set_return(self):
        self.current_function.has_return = True
        self.broadcast(Event(CompilerEvent.SET_RETURN,
                       self.current_function.type_))

    def __validate_return(self):
        if not self.current_function.valid_function():
            void_error = f'Void function should not return a value'
            type_error = f'Function should return {self.current_function.type_.value}'

            error = CompilerError(
                void_error if self.current_function.type_ is ValueType.VOID else type_error,
                trace=self.current_trace()
            )
            self.broadcast(Event(CompilerEvent.STOP_COMPILE, error))
        return None

    def get_output_function_data(self):
        """ Returns function_data dictionary used in output file """
        data = {}
        for id_, function_data in self.function_data_table.items():
            data[id_] = jsonpickle.encode(function_data)
        return data
