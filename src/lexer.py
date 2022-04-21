from ply.lex import lex

FILENAME = 'animals.ty'

with open('programs/' + FILENAME, 'r') as file:
    data = file.read()

reserved = {
    'CLASS' : 'class',
    'FUNC'  : 'func',
    'VAR'   : 'var',
    'INT'   : 'Int',
    'FLOAT' : 'Float',
    'STRING': 'String',
    'BOOL'  : 'Bool',
    'TRUE'  : 'True',
    'FALSE' : 'False',
    'PRINT' : 'print',
    'IF'    : 'if',
    'ELSE'  : 'else',
    'WHILE' : 'while',
    'INPUT' : 'input',
    'RETURN': 'return'
}
tokens = [
# SYMBOLS
    'NLINE',
    'COLON',
    'COMMA',
    'PERIOD',
    'LPAREN',
    'RPAREN',
    'LCURLY',
    'RCURLY',
    'LBRACK',
    'RBRACK',
    'QUOTE',
    'BSLASH',
    'ARROW',
# RELATIONAL OPERATORS
    'AND',
    'OR',
    'LESS',
    'MORE',
    'EQUALS',
    'NEQUALS',
    'LEQUALS',
    'MEQUALS',
# OPERATORS
    'PLUS',
    'MINUS',
    'TIMES',
    'DIVIDE',
    'ASSIGN',
# REGEX
    'ID',
    'NUMBER',
    'DECIMAL',
    'CHARS'
] + list(reserved.values())

# Symbol rules
t_NLINE     = r'\n'
t_COLON     = ':'
t_COMMA     = ','
t_PERIOD    = '.'
t_LPAREN    = r'\('
t_RPAREN    = r'\)'
t_LCURLY    = r'\{'
t_RCURLY    = r'\}'
t_LBRACK    = r'\['
t_RBRACK    = r'\]'
t_QUOTE     = '"'
t_BSLASH    = r'\\'
t_ARROW     = '->'
# Relational operator rules
t_AND       = '&&'
t_OR        = '\|\|'
t_LESS      = '<'
t_MORE      = '>'
t_EQUALS    = '=='
t_NEQUALS   = '!='
t_LEQUALS   = '<='
t_MEQUALS   = '>='
# Operator rules
t_PLUS      = r'\+'
t_MINUS     = '-'
t_TIMES     = r'\*'
t_DIVIDE    = r'\/'
t_ASSIGN    = '='

# Regex rules
def t_ID(t):
    r'[a-zA-Z0-9_]+'
    t.type = reserved.get(t.value,'ID')     # Check for reserved words
    return t

def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_DECIMAL(t):
    r'\d+.\d+'
    t.value = float(t.value)
    return t

def t_CHARS(t):
    # Every character except " and \
    #r'[^"\]'
    # TODO
    r'aaa'
    return t


# Ignored characters
t_ignore = ' \t'

# Error handler for illegal characters
def t_error(t):
    print(f'Illegal character {t.value[0]!r}')
    t.lexer.skip(1)

lexer = lex()

# TEST

lexer.input(data)

# Tokenize
while True:
    tok = lexer.token()
    if not tok:
        break # no more input
    print(tok)