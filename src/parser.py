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


# -- PARAMS -----------------------


def p_params(p):
    '''
    params : LPAREN params1 RPAREN
           | LPAREN RPAREN
    '''


def p_params1(p):
    '''
    params1 : param
            | param COMMA params1
    '''


def p_param(p):
    '''
    param : ID COLON type
    '''


# -- BLOCKS -----------------------


def p_class_block(p):
    '''
    class_block : LCURLY class_block1 RCURLY
    '''


def p_class_block1(p):
    '''
    class_block1 : class_block2
                 | class_block3 class_block2
    '''


def p_class_block2(p):
    '''
    class_block2 : NLINE class_block1
                 | NLINE
    '''


def p_class_block3(p):
    '''
    class_block3 : function
                 | declaration
    '''


def p_init_block(p):
    '''
    init_block : LCURLY init_block1 RCURLY
    '''


def p_init_block1(p):
    '''
    init_block1 : init_block2
                | init_block3 init_block2
    '''


def p_init_block2(p):
    '''
    init_block2 : NLINE init_block1
                | NLINE
    '''


def p_init_block3(p):
    '''
    init_block3 : statement
                | declaration
    '''


def p_block(p):
    '''
    block : LCURLY block1 RCURLY
    '''


def p_block1(p):
    '''
    block1 : block2
           | statement block2
    '''


def p_block2(p):
    '''
    block2 : NLINE block1
           | NLINE
    '''


# -- STATEMENTS -----------------------

def p_statement(p):
    '''
    statement : display
              | if
              | while
              | input
              | assign
              | call
              | return
    '''


def p_while(p):
    '''
    while : WHILE LPAREN bool_expr RPAREN block
    '''


def p_input(p):
    '''
    input : variable ASSIGN INPUT LPAREN string RPAREN
    '''


def p_display(p):
    '''
    display : PRINT LPAREN expression RPAREN
    '''


def p_return(p):
    '''
    return : RETURN
           | RETURN bool_expr
    '''


def p_assign(p):
    '''
    assign : ID assign1 expression
    '''


def p_assign1(p):
    '''
    assign1 : ASSIGN
            | PASSIGN
            | LASSIGN
            | MASSIGN
            | DASSIGN
    '''


def p_call(p):
    '''
    call : ID LPAREN call1 RPAREN
    '''


def p_call1(p):
    '''
    call1 : expression
          | expression COMMA call1
    '''


def p_if(p):
    '''
    if : IF LPAREN bool_expr RPAREN block
       | IF LPAREN bool_expr RPAREN block if2
    '''


def p_if2(p):
    '''
    if2 : ELSE if
        | ELSE block
    '''


# -- EXPRESSIONS -----------------------

def p_bool_expr(p):
    '''
    bool_expr : relational_exp
              | relational_exp AND bool_expr
              | relational_exp OR bool_expr
    '''


def p_relational_exp(p):
    '''
    relational_exp : expression comp expression
                   | expression
    '''


def p_comp(p):
    '''
    comp : LESS
         | MORE
         | EQUALS
         | NEQUALS
         | LEQUALS
         | MEQUALS
    '''


def p_expression(p):
    '''
    expression : term
               | term PLUS term
               | term MINUS term
    '''


def p_term(p):
    '''
    term : factor
         | factor TIMES factor
         | factor DIVIDE factor
    '''


def p_factor(p):
    '''
    factor : constant
           | COLON LPAREN expression RPAREN
    '''


def p_call_array(p):
    '''
    call_array : ID LBRACK expression RBRACK
    '''


def p_constant(p):
    '''
    constant : constant2
             | NUMBER
             | FLOATLIT
             | TRUE
             | FALSE
             | string
             | call
             | call_array
    '''


def p_constant2(p):
    '''
    constant2 : ID
              | ID PERIOD constant2
    '''

# Sorry Paco, I changed the 'DOT' Token to 'PERIOD' and commented out
# this chunk of code. Maybe you are right, for now, let's just keep it simple :)
#
# def p_dots(p):
#     # we might need this kind of syntax for easier semantic eval
#     '''
#     dots : ID
#          | repeat_dots
#     '''
#
#
# def p_repeat_dots(p):
#     ''' repeat_dots : ID DOT right_id'''
#
#
# def p_right_id(p):
#     ''' right_id : ID
#         | repeat_dots'''


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


def p_error(p):
    if p is None:
        token = "end of file"
    else:
        token = f"{p.type}({p.value}) on line {p.lineno}"

    print(f"Syntax error: Unexpected {token}")


parser = yacc.yacc(debug=True)
