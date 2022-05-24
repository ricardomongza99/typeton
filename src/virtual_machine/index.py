from typing import List

from src.compiler.code_generator.type import Quad, OperationType
from src.virtual_machine.types import ContextMemory, SizeData


# TODO separate  functions (and make static) into a different files

class VirtualMachine:
    def __init__(self):
        self.quad_pointer = 0
        self.memory_allocator = SizeData(0, 0, 0, 0)  # controls limits

        self.quad_list: List[Quad] = []
        self.function_data_list = []
        self.global_memory = None
        self.constant_memory = None
        self.context_memory_stack: List[ContextMemory] = []

    def load_data(self, json_bytecode):
        print("hello world")
        # load_constant_table()
        # load_quad_list()
        # load_directory()
        # load_memory_data()

    def run(self):
        while self.quad_pointer < len(self.quad_list) - 1:
            self.execute_quad()

    def execute_quad(self):
        quad = self.quad_list[self.quad_pointer]
        self.__execute_sequential_operation(quad)

    def __execute_sequential_operation(self, quad):
        memory = self.context_memory_stack[-1]
        left = memory.get(quad.left_address)
        right = memory.get(quad.right_address)
        result = 0

        if quad.operation is OperationType.ADD:
            result = left + right
        elif quad.operation is OperationType.SUBTRACT:
            result = left - right
        elif quad.operation is OperationType.MULTIPLY:
            result = left * right
        elif quad.operation is OperationType.DIVIDE:
            result = left / right
        else:
            self.__execute_boolean_expression(quad)

        self.quad_pointer += 1
        self.__execute__assign(quad.result_address, result)

    def __execute_boolean_expression(self, quad):
        memory = self.context_memory_stack[-1]
        left = memory.get(quad.left_address)
        right = memory.get(quad.right_address)
        result = 0

        if quad.operation is OperationType.AND:
            result = left and right
        elif quad.operation is OperationType.OR:
            result = left or right
        elif quad.operation is OperationType.EQUAL:
            result = left == right
        elif quad.operation is OperationType.LESS_THAN:
            result = left < right
        elif quad.operation is OperationType.GREAT_THAN:
            result = left > right
        elif quad.operation is OperationType.LESS_EQUAL:
            result = left <= right
        elif quad.operation is OperationType.GREAT_EQUAL:
            result = left >= right
        else:
            self.__execute_builtin_functions(quad)

        self.quad_pointer += 1
        self.__execute__assign(quad.result_address, result)

    def __execute_builtin_functions(self, quad):
        memory = self.context_memory_stack[-1]

        if quad.operation is OperationType.PRINT:
            print(memory.get(quad.result_address))
        else:
            self.__execute_conditional_operation(quad)

    def __execute_conditional_operation(self, quad):
        memory = self.context_memory_stack[-1]

        if quad.operation is OperationType.GOTO:
            self.quad_pointer = quad.right_address
        elif quad.operation is OperationType.GOTOF:
            if memory.get(quad.right_address) is False:
                self.quad_pointer = quad.result_address
        elif quad.operation is OperationType.GOTOV:
            if memory.get(quad.right_address) is True:
                self.quad_pointer = quad.result_address
        else:
            self.__execute_function_calls(quad)

    def __execute_function_calls(self, quad):
        pass

    def __execute__assign(self, address, value):
        self.context_memory_stack[-1].save(address, value)
