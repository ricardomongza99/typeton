import ply.yacc as yacc
from lexer import lexer, tokens


#blocks --------------------------------------------------


#base block: allows statements
def p_block(p):
    ''' block : LCURLY repeat_block RCURLY'''

def p_repeat_block(p):
    ''' repeat_block : block_content NLINE repeat_block'''

def p_block_content(p):
    ''' block_content : statement | '''

#init block: allows statements and declarations

def p_init_block(p):
    ''' init_block : LCURLY repeat_init_block RCURLY'''

def p_repeat_init_block(p):
    ''' repeat_init_block : init_block_content NLINE repeat_init_block'''

def p_init_block_content(p):
    ''' init_block_content : statement | declaration | '''

#class block: allows functions and declarations

def p_class_block(p):
    ''' class_block : LCURLY repeat_class_block RCURLY'''

def p_repeat_class_block(p):
    ''' repeat_class_block : class_block_content NLINE repeat_class_block'''

def p_class_block_content(p):
    ''' class_block_content : function | declaration | '''

#blocks --------------------------------------------------



#params --------------------------------------------------


def p_params(p):
    ''' params : LPAREN params_content RPAREN '''

def p_params_content(p):
    ''' params_content : param | param COMMA params_content | '''

def p_param(p):
    ''' param : ID COLON type'''


#params --------------------------------------------------


def p_program(p):
    ''' program : repeat_program '''

def p_repeat_program(p):
        ''' repeat_program : program_options NLINE repeat_program'''

def p_program_options(p):
    ''' program_options : class | function | declaration | '''




parser = yacc.yacc(debug=True)