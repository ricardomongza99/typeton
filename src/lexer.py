import ply.lex as lex

reserved = {
    'class' : 'CLASS',
    'func'  : 'FUNC',
    'var'   : 'VAR',
    'Int'   : 'INT',
    'Float' : 'FLOAT',
    'String': 'STRING',
    'Bool'  : 'BOOL',
    'true'  : 'TRUE',
    'false' : 'FALSE',
    'print' : 'PRINT',
    'if'    : 'IF',
    'else'  : 'ELSE',
    'while' : 'WHILE',
    'input' : 'INPUT',
    'return': 'RETURN'
}

tokens = [
# SYMBOLS
    'NLINE',
    'COLON',
    'COMMA',
    'DOT',
    'LPAREN',
    'RPAREN',
    'LCURLY',
    'RCURLY',
    'LBRACK',
    'RBRACK',
    # 'QUOTE',
    'BSLASH',
    'ARROW',
# RELATIONAL OPERATORS
    'AND',
    'OR',
    'LESS',
    'MORE',
    'EQUALS',
    'NEQUALS',
    'PASSIGN',
    'LASSIGN',
    'MASSIGN',
    'DASSIGN',
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
    'FLOATLIT',
    'STRINGLIT'
] + list(reserved.values())

# Symbol rules
t_COLON     = ':'
t_COMMA     = ','
t_DOT    = '\.'
t_LPAREN    = r'\('
t_RPAREN    = r'\)'
t_LCURLY    = r'\{'
t_RCURLY    = r'\}'
t_LBRACK    = r'\['
t_RBRACK    = r'\]'
# t_QUOTE     = '"'
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

t_PASSIGN   = '\+='
t_LASSIGN   = '\-='
t_MASSIGN   = '\*='
t_DASSIGN = '\/='

# Operator rules
t_PLUS      = r'\+'
t_MINUS     = '-'
t_TIMES     = r'\*'
t_DIVIDE    = r'\/'
t_ASSIGN    = '='

precedence = (
    ('left', '+', '-'),
    ('left', '*', '/'),
    ('right', 'UMINUS'),
)

# Regex rules
def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value, 'ID')     # Check for reserved words
    return t

def t_FLOATLIT(t):
    r'\d+.\d+'
    t.type = "FLOATLIT"
    t.value = float(t.value)
    return t

def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_STRINGLIT(t):
    # [^"] = Every character except "
    r'\"[^"]*\"'
    t.type = 'STRINGLIT'
    t.value = t.value     # remove quotes
    return t

def t_NLINE(t):
    r'\n+'
    t.lexer.lineno += len(t.value)
    t.value = 'newline'
    return t

# Ignored characters
t_ignore = ' \t'

# Error handler for illegal characters
def t_error(t):
    print("invalid character: ", t.value[0])
    t.lexer.skip(1)

lexer = lex.lex()

