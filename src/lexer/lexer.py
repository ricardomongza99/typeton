from src.ply import lex

reserved = {
    'class': 'CLASS',
    'func': 'FUNC',
    'var': 'VAR',
    'Int': 'INT',
    'Float': 'FLOAT',
    'String': 'STRING',
    'Bool': 'BOOL',
    'print': 'PRINT',
    'if': 'IF',
    'else': 'ELSE',
    'while': 'WHILE',
    'input': 'INPUT',
    'return': 'RETURN'
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
             'INTLIT',
             'BOOLLIT',
             'FLOATLIT',
             'STRINGLIT'
         ] + list(reserved.values())

# Symbol rules
t_COLON = ':'
t_COMMA = ','
t_PERIOD = '\.'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LCURLY = r'\{'
t_RCURLY = r'\}'
t_LBRACK = r'\['
t_RBRACK = r'\]'
# t_QUOTE     = '"'
t_BSLASH = r'\\'
t_ARROW = '->'
# Relational operator rules
t_AND = '&&'
t_OR = r'\|\|'
t_LESS = '<'
t_MORE = '>'
t_EQUALS = '=='
t_NEQUALS = r'!='
t_LEQUALS = r'<='
t_MEQUALS = r'>='

t_PASSIGN = r'\+='
t_LASSIGN = r'\-='
t_MASSIGN = r'\*='
t_DASSIGN = r'\/='

# Operator rules
t_PLUS = r'\+'
t_MINUS = '-'
t_TIMES = r'\*'
t_DIVIDE = r'\/'
t_ASSIGN = '='

precedence = (
    ('left', '+', '-'),
    ('left', '*', '/'),
    ('right', 'UMINUS'),
)


def t_BOOLLIT(t):
    r'true|false'
    t.type = "BOOLLIT"
    return t


# Regex rules
def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value, 'ID')  # Check for reserved words
    return t


def t_FLOATLIT(t):
    r'\d+\.\d+'
    t.type = "FLOATLIT"
    t.value = float(t.value)
    return t


def t_INTLIT(t):
    r'\d+'
    t.value = int(t.value)
    return t


def t_STRINGLIT(t):
    # [^"] = Every character except "
    r'\"[^"]*\"'
    t.type = 'STRINGLIT'
    t.value = t.value  # remove quotes
    return t


def t_NLINE(t):
    r'\n'
    t.lexer.lineno += 1
    t.value = 'newline'
    return t


# Ignored characters
t_ignore = ' \t'


# Error handler for illegal characters
def t_error(t):
    print("invalid character: ", t.value[0])
    t.lexer.skip(1)


lexer = lex.lex()
