from typing import Dict, List

from src.parser.errors import CompilerError
from src.semantic.expression import Operand
from src.semantic.quadruple import Quad, OperationType
from src.semantic.type import ActionResult
from src.virtual.types import ValueType

"""
Conditional semantic actions
"""


class ConditionalActions:
    def __init__(self, quad_list):
        self.goto_jumps = []
        self.goto_f_jumps = []
        self.quad_list = quad_list

    def get_conditional(self, operand_list, quad_list): #get conditional
        expression: Operand = operand_list.pop()
        if expression.type_ is not ValueType.BOOL:
            return ActionResult(error=CompilerError("Type Error, if expression should be boolean"))

        quad = Quad(operation=OperationType.GOTOF, left_address=expression.address, right_address=None)
        self.goto_f_jumps.append(len(quad_list))  # current quad
        return ActionResult(quad)

    def fill_and_goto(self): # used after each else / elseif to fill gotof
        self.__fill_gotof()
        if len(self.goto_jumps) > 0:
            self.__fill_goto()

        goto_quad = Quad(operation=OperationType.GOTO, left_address=OperationType.GOTO, result_address=None)
        self.goto_jumps.append(len(self.quad_list))
        return ActionResult(goto_quad)

    def fill_end(self): # used to fill last goto
        index = self.goto_jumps.pop()
        self.quad_list[index].result_address = len(self.quad_list)  # next quad

    def __fill_gotof(self):
        pending_jump_index = self.goto_f_jumps.pop()
        self.quad_list[pending_jump_index].result_address = len(self.quad_list) + 1

    def __fill_goto(self):
        print("filling goto")
        pending_jump_index = self.goto_jumps.pop()
        self.quad_list[pending_jump_index].result_address = len(self.quad_list)
