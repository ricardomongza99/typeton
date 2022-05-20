from typing import List

from src.directory.constants import ConstantTable
from src.directory.function_table import FunctionTable
from src.parser.errors import CompilerError
from src.semantic.cube import check as check_type
from src.semantic.quadruple import Quad, OperationType
from src.singleton.debug import Debug
from src.utils.display import make_table, TableOptions
from src.virtual.compilation import Scheduler
from src.virtual.helpers import Layers
from src.virtual.types import ValueType


class Operator:
    def __init__(self, priority: int, type_: OperationType):
        self.priority = priority
        self.type_ = type_


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
        if operator.type_ == OperationType.LPAREN:
            self.parenthesis_start.append(len(self.__operator_stack))
            return True
        elif operator.type_ == OperationType.RPAREN:
            self.execute_remaining()
            self.parenthesis_start.pop()
            return True
        return False

    def display(self):
        address_map = Debug.get_map()

        table = make_table("Quadruples",
                           ["Operator", "Left", "Right", "Result"],
                           map(lambda quad:
                               [
                                   '{:^10}'.format(quad.operation.value),
                                   '{:<5} -->{:>5}'.format(address_map[quad.left_address], quad.left_address),
                                   '{:<5} --> {:<5}'.format(address_map[quad.right_address], quad.right_address)
                                   if address_map.get(quad.right_address) is not None else "....",
                                   '{:<5} -->{:>5}'.format(address_map[quad.result_address], quad.result_address)

                               ], self.__quad_list),
                           options=TableOptions(20, 20)
                           )
        print(table)

    def push_variable(self, id_):
        address, type_ = self.directory.find(id_)
        if address is None:
            return CompilerError(f'Variable "{id_}" not found')

        operand = Operand(type_, address)
        self.__operand_address_stack.append(operand)
        return None

    def execute_if_possible(self, priority):
        last_operator: Operator = self.peek_operators()
        if last_operator is not None and last_operator.priority == priority:
            return self.execute_arithmetic()
        return None

    def push_operator(self, new_operator: Operator):
        if self.handle_parenthesis(new_operator):
            return

        self.__operator_stack.append(new_operator)

    def execute_remaining(self):
        while len(self.__operator_stack) > self.parenthesis_start[-1] and len(self.__operand_address_stack) > 2:
            self.execute_arithmetic()

    def execute_assign(self):
        right = self.__operand_address_stack.pop()
        print(right.type_)
        left = self.__operand_address_stack.pop()

        address_map = Debug.get_map()
        type_match = check_type(OperationType.ASSIGN.value, left.type_.value, right.type_.value)
        if type_match is None:
            return CompilerError(
                f'Type: {address_map[left.address]}:{left.type_.value} {OperationType.ASSIGN.value} {address_map[right.address]} ({left.type_.value} and {right.type_.value} are not compatible)')

        quad = Quad(
            left_address=right.address,
            right_address=None,
            operation=OperationType.ASSIGN,
            result_address=left.address)

        self.__quad_list.append(quad)
        if not self.scheduler.is_segment(right.address, Layers.CONSTANT):
            self.scheduler.release_address(right.address)
        return None

    def execute_arithmetic(self):
        operator = self.__operator_stack.pop()

        if operator.type_ == OperationType.ASSIGN:
            return self.execute_assign()

        right: Operand = self.__operand_address_stack.pop()
        left = self.__operand_address_stack.pop()

        address_map = Debug.get_map()
        type_match = check_type(operator.type_.value, left.type_.value, right.type_.value)

        if type_match is None:
            return CompilerError(
                f'Type Mismatch: cannot perform action: {address_map[left.address]} {operator.type_.value} {address_map[right.address]}')

        result, error = self.scheduler.schedule_address(ValueType(type_match), Layers.TEMPORARY)

        self.__quad_list.append(Quad(
            left_address=left.address,
            right_address=right.address,
            operation=OperationType(operator.type_.value),  # convert to type for easy identification in vm
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
