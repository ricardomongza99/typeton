from typing import List

from src.directory import FunctionTable
from src.directory.constants import ConstantTable
from src.parser.errors import CompilerError
from src.semantic.cube import check as check_type
from src.semantic.quadruple import Quad, OperationType
from src.semantic.type import ActionResult, Operand, Operator
from src.singleton.debug import Debug
from src.virtual.compilation import Scheduler
from src.virtual.helpers import Layers
from src.virtual.types import ValueType


class ExpressionActions:
    def __init__(self, operands, operators):
        self.__operand_address_stack: List[Operand] = operands  # stores the
        # ed virtual address, not actual value
        self.__operator_stack: List[Operator] = operators
        self.parenthesis_start = [0]  # operators indexed before this value do not exist

    def push_variable(self, id_, directory: FunctionTable):
        address, type_ = directory.find(id_)
        if address is None:
            return ActionResult(error=CompilerError(f'Variable "{id_}" not found'))

        operand = Operand(type_, address)
        self.__operand_address_stack.append(operand)
        return ActionResult()

    def get_operands(self):
        return self.__operand_address_stack

    def execute_if_possible(self, priority, scheduler: Scheduler):
        last_operator: Operator = self.__peek_operators()

        if last_operator is not None and last_operator.priority == priority:
            if priority == 0:
                return self.__execute_assign(scheduler)
            return self.__execute_arithmetic(scheduler)
        return ActionResult()

    def push_operator(self, new_operator: Operator, scheduler: Scheduler):
        results = self.__handle_parenthesis(new_operator, scheduler)
        if results is not None:
            return results
        else:
            self.__operator_stack.append(new_operator)
            return ActionResult()

    def execute_remaining(self, scheduler: Scheduler):
        results = []
        while len(self.__operator_stack) > self.parenthesis_start[-1] and len(self.__operand_address_stack) > 2:
            results.append(self.__execute_arithmetic(scheduler))
        return results

    def push_constant(self, value, constant_table: ConstantTable):
        constant = constant_table.get(value)
        operand = Operand(constant.type_, constant.address)
        self.__operand_address_stack.append(operand)
        return ActionResult()

    # Helpers
    def __handle_parenthesis(self, operator: Operator, scheduler: Scheduler):
        if operator.type_ == OperationType.LPAREN:
            self.parenthesis_start.append(len(self.__operator_stack))
            return ActionResult()
        elif operator.type_ == OperationType.RPAREN:
            results = self.execute_remaining(scheduler)
            self.parenthesis_start.pop()
            return results
        return None

    def __execute_assign(self, scheduler: Scheduler):
        operator = self.__operator_stack.pop()
        right = self.__operand_address_stack.pop()
        left = self.__operand_address_stack.pop()

        address_map = Debug.get_map()

        type_match = check_type(operator.type_.value, left.type_.value, right.type_.value)
        if type_match is None:
            return ActionResult(error=CompilerError(
                f'{address_map[left.address]}:'
                f'{left.type_.value} '
                f'{operator.type_.value} '
                f'{address_map[right.address]} '
                f'({left.type_.value} and {right.type_.value} are not compatible)'))

        quad = Quad(
            left_address=right.address,
            right_address=None,
            operation=OperationType.ASSIGN,
            result_address=left.address)

        if not scheduler.is_segment(right.address, Layers.CONSTANT):
            scheduler.release_address(right.address)

        return ActionResult(quad=quad)

    def __execute_arithmetic(self, scheduler: Scheduler):
        operator = self.__operator_stack.pop()

        right: Operand = self.__operand_address_stack.pop()
        left: Operand = self.__operand_address_stack.pop()

        address_map = Debug.get_map()
        type_match = check_type(operator.type_.value, left.type_.value, right.type_.value)

        if type_match is None:
            return ActionResult(error=CompilerError(
                f'Type Mismatch: cannot perform action: {address_map[left.address]} {operator.type_.value} {address_map[right.address]}'))

        result, error = scheduler.schedule_address(ValueType(type_match), Layers.TEMPORARY)
        self.__operand_address_stack.append(Operand(ValueType(type_match), result))

        quad = (Quad(
            left_address=left.address,
            right_address=right.address,
            operation=OperationType(operator.type_.value),  # convert to type for easy identification in vm
            result_address=result))

        # Release temp addresses
        if scheduler.is_segment(left.address, Layers.TEMPORARY):
            scheduler.release_address(left.address)
        if scheduler.is_segment(right.address, Layers.TEMPORARY):
            scheduler.release_address(right.address)

        return ActionResult(quad=quad)

    def __peek_operators(self, ):
        if len(self.__operator_stack) - 1 < self.parenthesis_start[-1]:
            return None
        return self.__operator_stack[-1]
