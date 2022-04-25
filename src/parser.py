import ply.yacc as yacc
from lexer import lexer, tokens


# blocks --------------------------------------------------

# base block: allows statements
def p_block(p):
    ''' block : LCURLY repeat_block RCURLY'''


def p_repeat_block(p):
    ''' repeat_block : block_content NLINE repeat_block'''


def p_block_content(p):
    ''' block_content : statement | '''


# init block: allows statements and declarations

def p_init_block(p):
    ''' init_block : LCURLY repeat_init_block RCURLY'''


def p_repeat_init_block(p):
    ''' repeat_init_block : init_block_content NLINE repeat_init_block'''


def p_init_block_content(p):
    ''' init_block_content : statement | declaration | '''


# class block: allows functions and declarations

def p_class_block(p):
    ''' class_block : LCURLY repeat_class_block RCURLY'''


def p_repeat_class_block(p):
    ''' repeat_class_block : class_block_content NLINE repeat_class_block'''


def p_class_block_content(p):
    ''' class_block_content : function | declaration | '''


# blocks --------------------------------------------------


# params --------------------------------------------------


def p_params(p):
    ''' params : LPAREN params_content RPAREN '''


def p_params_content(p):
    ''' params_content : param | param COMMA params_content | '''


def p_param(p):
    ''' param : ID COLON type'''


# params --------------------------------------------------

# program --------------------------------------------------

def p_program(p):
    ''' program : repeat_program '''


def p_repeat_program(p):
    ''' repeat_program : program_options NLINE repeat_program'''


def p_program_options(p):
    ''' program_options : class | function | declaration | '''


# program --------------------------------------------------

# variables --------------------------------------------------

def p_variable(p):
    ''' variable : VAR ID variable_content '''


def p_variable_content(p):
    ''' variable_content : COLON type |  '''


def p_type(p):
    ''' type : ID | primitive | LBRACKET primitive RBRACKET '''


def p_primitive(p):
    ''' primitive : INT | FLOAT | STRING | BOOL '''


def p_string(p):
    ''' string : QUOTE repeat_string QUOTE'''


def p_repeat_string(p):
    ''' repeat_string : string_expr | string_expr repeat_string'''


def p_string_expr(p):
    ''' string_expr : string | BSLASH LPAREN expression RPAREN '''


# variables --------------------------------------------------

# top_level --------------------------------------------------

def p_class(p):
    ''' class : class ID class_content class_block'''


def p_class_content(p):
    ''' class_content : COLON ID | '''


def p_function(p):
    ''' function : func ID params function_content init_block'''


def p_function_content(p):
    ''' function_content : ARROW primitive | '''


def p_declaration(p):
    ''' declaration : variable ASSIGN expression | variable ASSIGN array '''


def p_array(p):
    ''' array : LBRACK repeat_array RBRACK'''


def p_error(p):
    print("syntax error, at char: ", p.value[0])


def p_repeat_array(p):
    ''' repeat_array : expression | expression COMMA repeat_array '''


# top_level --------------------------------------------------

# expressions --------------------------------------------------

def p_bool_exp(p):
    ''' bool_exp : relational_exp
        | relational_exp AND bool_exp
        | relational_exp OR bool_exp '''


def p_relational_exp(p):
    ''' relational_exp : expression comp expression
        | BOOLEAN'''


def p_comp(p):
    ''' comp : LESS | MORE | EQUALS | NEQUALS | LEQUALS | MEQUALS '''


def p_expression(p):
    ''' expression : term
        | term PLUS expression
        | term MINUS expression '''


def p_term(p):
    ''' term : factor
        | factor TIMES term
        | factor DIVIDE term '''


def p_factor(p):
    ''' factor : constant : LPAREN expression RPAREN '''


def p_call_array(p):
    ''' call_array : ID LBRACK expression RBRACK '''


def p_constant(p):
    ''' constant : dots | DECIMAL | BOOLEAN | NUMBER | string | call | call_array '''


# we might need this kind of syntax for easier semantic eval
def p_dots(p):
    ''' dots : ID | repeat_dots'''


def p_repeat_dots(p):
    ''' repeat_dots : ID DOT right_id'''


def p_right_id(p):
    ''' right_id : ID | repeat_dots '''


# expressions --------------------------------------------------

# statements --------------------------------------------------

def p_statement(p):
    ''' statement : display | if | while | for | input | call | return '''


def p_while(p):
    ''' while : WHILE LPAREN bool_expr RPAREN block'''


def p_input(p):
    ''' input : variable ASSIGN INPUT LPAREN string RPAREN '''


def p_display(p):
    ''' display : PRINT LPAREN expression RPAREN '''


def p_return(p):
    ''' return : RETURN | RETURN bool_expr | RETURN expression '''


def p_assign(p):
    ''' assign : ID some_op expression '''


def p_some_op(p):
    ''' some_op : ASSIGN | PASSIGN | LASSIGN | MASSIGN | DASSIGN'''


# statements --------------------------------------------------


parser = yacc.yacc(debug=True)
