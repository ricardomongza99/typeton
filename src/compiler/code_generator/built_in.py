from src.compiler.code_generator.expression import Operand, Operator, OperationType, ValueType, Layers, FunctionTableEvents
from src.compiler.code_generator.type import Quad
from src.compiler.errors import CompilerError, CompilerEvent
from src.compiler.stack_allocator.index import StackAllocator
from src.utils.observer import Publisher, Event

"""
Conditional semantic actions
"""


class Builtin_Function_Actions(Publisher):
    def __init__(self, quad_list):
        super().__init__()
        self.quad_list = quad_list

    def execute_call(self, operators, operands, stack_allocator):
        operator: Operator = operators.pop()

        if operator.type_ is operator.type_.PRINT:
            return self.execute_print(operator, operands)
        elif operator.type_ is operator.type_.INPUT:
            self.execute_input(operands, stack_allocator)

    def execute_print(self, operator, operands):
        if len(operands) == 0:
            self.broadcast(Event(CompilerEvent.STOP_COMPILE, CompilerError(f'variable is not initialized')))
        expression: Operand = operands.pop()

        quad = Quad(operation=operator.type_.value, result_address=expression.address)
        self.quad_list.append(quad)

    def execute_input(self, operands, stack_allocator: StackAllocator):
        operand: Operand = operands[-1]

        temp_address = stack_allocator.allocate_address(operand.type_, Layers.TEMPORARY)
        quad = Quad(operation=OperationType.INPUT, result_address=temp_address)
        self.quad_list.append(quad)

        operands.append(Operand(type_=operand.type_, address=temp_address))

        # TODO: broadcast temp
        self.broadcast(
            Event(
                FunctionTableEvents.ADD_TEMP,
                (operand.type_, temp_address, None)
            )
        )
