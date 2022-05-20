from typing import List

from src.directory.constants import ConstantTable
from src.directory.function_table import FunctionTable
from src.semantic.cube import check as check_type
from src.semantic.quadruple import Quad, OperationType
from src.singleton.debug import Debug
from src.utils.display import make_table, TableOptions
from src.virtual.compilation import Scheduler
from src.virtual.helpers import Layers
from src.virtual.types import ValueType


class Operator:
    def __init__(self, priority: int, value):
        self.priority = priority
        self.value = value


class Operand:
    def __init__(self, type_: ValueType, address: int):
        self.type_ = type_
        self.address = address


class QuadGenerator:
    def __init__(self, scheduler: Scheduler, directory: FunctionTable):
        self.__operand_address_stack: List[Operand] = []  # stores the assigned virtual address, not actual value
        self.__operator_stack: List[Operator] = []
        self.__quad_list: List[Quad] = []
        self.directory = directory
        self.parenthesis_start = [0]  # operators indexed before this value do not exist
        self.scheduler = scheduler

    def handle_parenthesis(self, operator: Operator):
        if operator.value == OperationType.LPAREN.value:
            self.parenthesis_start.append(len(self.__operator_stack))
            return True
        elif operator.value == OperationType.RPAREN.value:
            self.parenthesis_start.pop()
            return True
        return False

    def display(self):
        debug = Debug.get_instance().get_map()

        table = make_table("Quadruples",
                           ["Operator", "Left", "Right", "Result"],
                           map(lambda quad:
                               [
                                   '{:^10}'.format(quad.operation.value),
                                   '{:<5} -->{:>5}'.format(debug[quad.left_address], quad.left_address),
                                   '{:<5} --> {:<5}'.format(debug[quad.right_address], quad.right_address)
                                   if debug.get(quad.right_address) is not None else "....",
                                   '{:<5} -->{:>5}'.format(debug[quad.result_address], quad.result_address)

                               ], self.__quad_list),
                           options=TableOptions(20, 20)
                           )
        print(table)

    def push_variable(self, id_):
        address, type_ = self.directory.find(id_)
        operand = Operand(type_, address)
        self.__operand_address_stack.append(operand)

    def execute_if_possible(self, priority):
        last_operator: Operator = self.peek_operators()
        if last_operator is not None and last_operator.priority == priority:
            self.execute_arithmetic()

    def push_operator(self, new_operator: Operator):
        if self.handle_parenthesis(new_operator):
            return

        last_operator: Operator = self.peek_operators()
        if last_operator is not None and last_operator.priority >= new_operator.priority:
            self.execute_arithmetic()
        self.__operator_stack.append(new_operator)

    def execute_remaining(self):
        while len(self.__operator_stack) > 0:
            self.execute_arithmetic()

    def execute_assign(self):
        right = self.__operand_address_stack.pop()
        left = self.__operand_address_stack.pop()
        quad = Quad(
            left_address=right.address,
            right_address=None,
            operation=OperationType.ASSIGN,
            result_address=left.address)

        self.__quad_list.append(quad)

        if not self.scheduler.is_segment(right.address, Layers.CONSTANT):
            self.scheduler.release_address(right.address)

    def execute_arithmetic(self):
        operator = self.__operator_stack.pop()

        if operator.value == OperationType.ASSIGN.value:
            self.execute_assign()
            return

        right: Operand = self.__operand_address_stack.pop()
        left = self.__operand_address_stack.pop()

        type_match = check_type(operator.value, left.type_.value, right.type_.value)
        if type_match is None:
            print('error')

        result, error = self.scheduler.schedule_address(ValueType(type_match), Layers.TEMPORARY)

        self.__quad_list.append(Quad(
            left_address=left.address,
            right_address=right.address,
            operation=OperationType(operator.value),  # convert to type for easy identification in vm
            result_address=result))

        self.__operand_address_stack.append(Operand(ValueType(type_match), result))

        # Release temp addresses
        if self.scheduler.is_segment(left.address, Layers.TEMPORARY):
            self.scheduler.release_address(left.address)
        if self.scheduler.is_segment(right.address, Layers.TEMPORARY):
            self.scheduler.release_address(right.address)

    def peek_operators(self, ):
        if len(self.__operator_stack) - 1 < self.parenthesis_start[-1]:
            return None
        return self.__operator_stack[-1]

    def push_constant(self, value, constant_table: ConstantTable):
        constant = constant_table.get(value)
        operand = Operand(constant.type_, constant.address)
        self.__operand_address_stack.append(operand)
