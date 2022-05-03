import ply.yacc as yacc
from lexer import lexer, tokens


# -- PROGRAM -----------------------

def p_program(p):
    '''
    program : program1 program
            | program1
    '''

def p_program1(p):
    '''
    program1 : body NLINE
             | NLINE
    '''

def p_body(p):
    '''
    body : class
         | function
         | declaration
    '''


# -- TOP LEVEL -----------------------

def p_class(p):
    '''
    class : CLASS ID class_block
          | CLASS ID COLON ID class_block
    '''


def p_function(p):
    '''
    function : FUNC ID params init_block
             | FUNC ID params ARROW primitive init_block
    '''


def p_declaration(p):
    '''
    declaration : variable ASSIGN expression
                | variable ASSIGN array
                | variable
    '''


def p_array(p):
    '''
    array : LBRACK array1 RBRACK
    '''


def p_array1(p):
    '''
    array1 : expression COMMA array1
           | expression
    '''


# -- BLOCKS -----------------------

def p_block(p):
    # base block: allows statements
    ''' block : LCURLY NLINE repeat_block RCURLY'''


def p_repeat_block(p):
    ''' repeat_block : statement NLINE repeat_block
        |'''


def p_init_block(p):
    # allows statements and declarations
    ''' init_block : LCURLY NLINE repeat_init_block RCURLY'''


def p_repeat_init_block(p):
    ''' repeat_init_block : init_block_content NLINE repeat_init_block
        |'''


def p_init_block_content(p):
    ''' init_block_content : statement
        | declaration'''


def p_class_block(p):
    # class block: allows functions and declarations
    ''' class_block : LCURLY NLINE repeat_class_block RCURLY'''


def p_repeat_class_block(p):
    ''' repeat_class_block : class_block_content NLINE repeat_class_block
        |'''


def p_class_block_content(p):
    ''' class_block_content : declaration
        | function'''


# -- PARAMS -----------------------


def p_params(p):
    ''' params : LPAREN params_content RPAREN '''


def p_params_content(p):
    ''' params_content : param
        | param COMMA params_content
        |'''


def p_param(p):
    ''' param : ID COLON type'''


# -- VARIABLES -----------------------

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


# -- EXPRESSIONS -----------------------

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


def p_dots(p):
    # we might need this kind of syntax for easier semantic eval
    ''' dots : ID
        | repeat_dots'''


def p_repeat_dots(p):
    ''' repeat_dots : ID DOT right_id'''


def p_right_id(p):
    ''' right_id : ID
        | repeat_dots'''


# -- STATEMENTS -----------------------

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
    if p is None:
        token = "end of file"
    else:
        token = f"{p.type}({p.value}) on line {p.lineno}"

    print(f"Syntax error: Unexpected {token}")


parser = yacc.yacc(debug=True)
