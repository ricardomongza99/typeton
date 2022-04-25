import ply.yacc as yacc
from lexer import lexer, tokens


#blocks --------------------------------------------------


#base block: allows statements
def p_block(p):
    ''' block : LCURLY repeat_block NLINE RCURLY'''

def p_repeat_block(p):
    ''' repeat_block : block_content repeat_block'''

def p_block_content(p):
    '''block_content : statement | '''

#init block: allows statements and declarations

def p_init_block(p):
    ''' init_block : LCURLY repeat_init_block NLINE RCURLY'''

def p_repeat_init_block(p):
    ''' repeat_init_block : init_block_content repeat_init_block'''

def p_init_block_content(p):
    ''' init_block_content : statement | declaration | '''

#class block: allows functions and declarations

def p_class_block(p):
    ''' init_block : LCURLY repeat_class_block NLINE RCURLY'''

def p_repeat_class_block(p):
    ''' repeat_class_block : class_block_content repeat_class_block'''

def p_class_block_content(p):
    ''' class_block_content : statement | function | '''

#blocks --------------------------------------------------



parser = yacc.yacc(debug=True)