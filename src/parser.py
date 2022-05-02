import ply.yacc as yacc
from lexer import lexer, tokens

# program --------------------------------------------------

def p_program(p):
    ''' program : repeat_program '''


def p_repeat_program(p):
    ''' repeat_program : program_options NLINE repeat_program
        |'''


def p_program_options(p):
    ''' program_options : class
        | function
        | declaration
        |'''


# program --------------------------------------------------



# blocks --------------------------------------------------

# base block: allows statements
def p_block(p):
    ''' block : LCURLY NLINE repeat_block RCURLY'''


def p_repeat_block(p):
    ''' repeat_block : statement NLINE repeat_block
        |'''


# init block: allows statements and declarations

def p_init_block(p):
    ''' init_block : LCURLY NLINE repeat_init_block RCURLY'''


def p_repeat_init_block(p):
    ''' repeat_init_block : init_block_content NLINE repeat_init_block
        |'''


def p_init_block_content(p):
    ''' init_block_content : statement
        | declaration'''


# class block: allows functions and declarations

def p_class_block(p):
    ''' class_block : LCURLY NLINE repeat_class_block RCURLY'''


def p_repeat_class_block(p):
    ''' repeat_class_block : class_block_content NLINE repeat_class_block
        |'''


def p_class_block_content(p):
    ''' class_block_content : declaration
        | function'''


# blocks --------------------------------------------------


# params --------------------------------------------------


def p_params(p):
    ''' params : LPAREN params_content RPAREN '''


def p_params_content(p):
    ''' params_content : param
        | param COMMA params_content
        |'''


def p_param(p):
    ''' param : ID COLON type'''


# params --------------------------------------------------

# variables --------------------------------------------------

def p_variable(p):
    ''' variable : VAR ID
        | VAR ID COLON type'''


def p_type(p):
    ''' type : primitive
        | ID
        | LBRACK primitive RBRACK
        | LBRACK ID RBRACK''' #might need to remove this array of custom types


def p_primitive(p):
    ''' primitive : INT
        | FLOAT
        | STRING
        | BOOL'''


def p_string(p):
    ''' string : string_expr
        | string_expr string'''


def p_string_expr(p):
    ''' string_expr : STRINGLIT
        | BSLASH LPAREN expression RPAREN'''


# variables --------------------------------------------------

# top_level --------------------------------------------------

def p_class(p):
    ''' class : CLASS ID class_content class_block'''


def p_class_content(p):
    ''' class_content : COLON ID
        |'''


def p_function(p):
    ''' function : FUNC ID params function_content init_block'''


def p_function_content(p):
    ''' function_content : ARROW primitive
        |'''


def p_declaration(p):
    ''' declaration : variable ASSIGN expression
        | variable ASSIGN array
        | variable'''


def p_array(p):
    ''' array : LBRACK repeat_array RBRACK'''


def p_repeat_array(p):
    ''' repeat_array : expression
        | expression COMMA repeat_array '''


# top_level --------------------------------------------------

# expressions --------------------------------------------------

def p_bool_expr(p):
    ''' bool_expr : relational_exp
        | relational_exp AND bool_expr
        | relational_exp OR bool_expr'''


def p_relational_exp(p):
    ''' relational_exp : expression comp expression
        | expression'''


def p_comp(p):
    ''' comp : LESS
        | MORE
        | EQUALS
        | NEQUALS
        | LEQUALS
        | MEQUALS'''


def p_expression(p):
    ''' expression : term
    | term PLUS term
    | term MINUS term'''


def p_term(p):
    ''' term : factor
      | factor DIVIDE factor
      | factor TIMES factor'''


def p_factor(p):
    ''' factor : constant
        | COLON LPAREN expression RPAREN'''


def p_call_array(p):
    ''' call_array : ID LBRACK expression RBRACK '''


def p_constant(p):
    ''' constant : dots
        | FLOATLIT
        | TRUE
        | FALSE
        | NUMBER
        | string
        | call
        | call_array'''


# we might need this kind of syntax for easier semantic eval
def p_dots(p):
    ''' dots : ID
        | repeat_dots'''


def p_repeat_dots(p):
    ''' repeat_dots : ID DOT right_id'''


def p_right_id(p):
    ''' right_id : ID
        | repeat_dots'''


# expressions --------------------------------------------------

# statements --------------------------------------------------

def p_statement(p):
    ''' statement : display
        | if
        | while
        | input
        | assign
        | call
        | return'''


def p_while(p):
    ''' while : WHILE LPAREN bool_expr RPAREN block'''


def p_input(p):
    ''' input : variable ASSIGN INPUT LPAREN string RPAREN '''


def p_display(p):
    ''' display : PRINT LPAREN expression RPAREN '''


def p_return(p):
    ''' return : RETURN
        | RETURN bool_expr'''


def p_assign(p):
    ''' assign : ID some_op expression '''


def p_some_op(p):
    ''' some_op : ASSIGN
        | PASSIGN
        | LASSIGN
        | MASSIGN
        | DASSIGN'''

def p_call(p):
    ''' call : ID LPAREN repeat_call RPAREN'''

def p_repeat_call(p):
    ''' repeat_call : expression
        | expression COMMA repeat_call
        |'''



def p_if(p):
    ''' if : IF LPAREN bool_expr RPAREN block if_content'''

def p_if_content(p):
    ''' if_content : ELSE if
        | ELSE block
        |'''


def p_error(p):
    if p == None:
        token = "end of file"
    else:
        token = f"{p.type}({p.value}) on line {p.lineno}"

    print(f"Syntax error: Unexpected {token}")

# statements --------------------------------------------------


parser = yacc.yacc(debug=True)
