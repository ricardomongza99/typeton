# expressions --------------------------------------------------

from src.parser.main import Compiler

def p_bool_expr(self, p):
    ''' bool_expr : relational_exp
        | relational_exp AND bool_expr
        | relational_exp OR bool_expr'''


def p_relational_exp(self, p):
    ''' relational_exp : expression comp expression
        | expression'''


def p_comp(self, p):
    ''' comp : LESS
        | MORE
        | EQUALS
        | NEQUALS
        | LEQUALS
        | MEQUALS'''


def p_expression(self, p):
    ''' expression : term
    | term PLUS term
    | term MINUS term'''


def p_term(self, p):
    ''' term : factor
      | factor DIVIDE factor
      | factor TIMES factor'''


def p_factor(self, p):
    ''' factor : constant
        | COLON LPAREN expression RPAREN'''


def p_call_array(self, p):
    ''' call_array : ID LBRACK expression RBRACK '''


def p_constant(self, p):
    ''' constant : dots
        | FLOATLIT
        | TRUE
        | FALSE
        | NUMBER
        | string
        | call
        | call_array'''


# we might need this kind of syntax for easier semantic eval
def p_dots(self, p):
    ''' dots : ID
        | repeat_dots'''


def p_repeat_dots(self, p):
    ''' repeat_dots : ID DOT right_id'''


def p_right_id(self, p):
    ''' right_id : ID
        | repeat_dots'''


# expressions --------------------------------------------------

funcs = [
    p_bool_expr,
    p_relational_exp,
    p_comp, p_expression,
    p_term, p_factor,
    p_call_array,
    p_constant,
    p_dots,
    p_repeat_dots,
    p_right_id
]