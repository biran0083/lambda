#!python3
from ply import lex
from ply import yacc

class Closure:
    def __init__(self, fun, env):
        self.fun = fun
        self.env = env

    def __call__(self, arg):
        return self.apply(arg)

    def apply(self, arg):
        new_env = self.env.copy()
        new_env[self.fun.arg] = arg
        return self.fun.body.eval(new_env)


class Exp:
    pass

class Variable(Exp):
    def __init__(self, name):
        self.name = name

    def eval(self, env):
        return env[self.name]

class Function(Exp):
    def __init__(self, arg, body):
        self.arg = arg
        self.body = body

    def eval(self, env):
        return Closure(self, env)


class Apply(Exp):
    def __init__(self, fun, param):
        self.fun = fun
        self.param = param

    def eval(self, env):
        arg = self.param.eval(env)
        f = self.fun.eval(env)
        return f(arg)
    
tokens = ('LPAREN', 'RPAREN', 'LAMBDA', 'COLON', 'VAR')

t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LAMBDA = 'lambda'
t_COLON = ':'
t_ignore = '[ \t\n\r]'

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


lexer = lex.lex()
parser = yacc.yacc()

def parse(s):
    res = parser.parse(s)
    return res


