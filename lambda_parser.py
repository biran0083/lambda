#!python3
from ply import lex, yacc   
from lambda_ast import *

tokens = ('LPAREN', 'RPAREN', 'LAMBDA', 'COLON', 'VAR')

t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LAMBDA = 'lambda'
t_COLON = ':'
t_ignore = ' \t\n\r'

def t_VAR(t):
    r'[_a-zA-Z][\w_]*'
    if t.value == 'lambda':
        t.type = 'LAMBDA'
    return t

def t_error(t):
    print(f'Illegal character {t.value[0]!r}')
    t.lexer.skip(1)

def p_exp_var(p):
    """
    exp : VAR
    """
    p[0] = Variable(p[1])

def p_exp_apply(p):
    """
    exp : exp LPAREN exp RPAREN
    """
    p[0] = Apply(p[1], p[3])

def p_exp_lambda(p):
    """
    exp : LAMBDA VAR COLON exp
    """
    p[0] = Function(p[2], p[4])

def p_exp_paren(p):
    """
    exp : LPAREN exp RPAREN
    """
    p[0] = p[2]

def p_error(p):
    print(f'Syntax error at {p.value!r}')


def parse(s):
    lexer = lex.lex()
    parser = yacc.yacc()
    res = parser.parse(s)
    return res


