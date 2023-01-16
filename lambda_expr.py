#!python3
import string
void = '(lambda x: x)'
true = f'(lambda true: (lambda false: true({void})))'
false = f'(lambda true: (lambda false: false({void})))'
nil = f'(lambda onPair: (lambda onNil: onNil({void})))'

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
    
class ParserBase:
    def __init__(self, exp):
        self.exp = exp
        self.i = 0
        self.token_buffer = []
        self.reserved_tokens = '():+-*'
        self.symbol_alphabet = string.ascii_lowercase + string.ascii_uppercase + string.digits + '_'

    def parse(self):
        pass

    def _has_more(self):
        return self.i < len(self.exp)

    def _current_char(self):
        return self.exp[self.i]

    def _advance(self):
        self.i += 1

    def _skip_space(self):
        while self._has_more() and self._current_char() == ' ':
            self._advance()
    
    def _push_back(self, token):
        self.token_buffer.append(token)

    def _parse_token(self):
        if self.token_buffer:
            return self.token_buffer.pop()
        self._skip_space()
        if not self._has_more():
            return None
        c = self._current_char()
        if c in self.reserved_tokens:
            self._advance()
            return c
        token = ''
        while self._has_more():
            c = self._current_char()
            if c in self.symbol_alphabet:
                token += c
                self._advance()
            else:
                break
        assert token, f'unknown token at {self.exp[self.i:]}'
        return token

class LambdaParser(ParserBase):

    def parse(self):
        token = self._parse_token()
        if token == 'lambda':
            arg = self._parse_token()
            assert(self._parse_token() == ':')
            body = self.parse()
            exp = Function(arg, body)
        elif token == '(':
            exp = self.parse()
            assert(self._parse_token() == ')')
        else:
            exp = Variable(token)
        while 1:
            token = self._parse_token()
            if not token:
                break
            if token != '(':
                assert(token == ')')
                self._push_back(token)
                break
            param = self.parse()
            assert(self._parse_token() == ')')
            exp = Apply(exp, param)
        return exp
                
                
def pair(exp1, exp2):
    return f'(lambda onPair: (lambda onNil: onPair({exp1})({exp2})))'

def first(exp):
    return f'{exp}(lambda fst: lambda rst: fst)({void})'

def rest(exp):
    return f'{exp}(lambda fst: lambda rst: rst)({void})'

def is_nil(exp):
    return f'{exp}(lambda fst: lambda rst: {false})(lambda x: {true})'

def is_zero(exp):
    return  f'{exp}(lambda x: {false})({true})'

def is_pair(exp):
    return f'{exp}(lambda fst: lambda rst: {true})(lambda x: {false})'

def natify_int_list(exp):
    res = []
    def helper(closure):
        def handle_rest(rst):
            helper(rst)

        def handle_first(fst):
            res.append(natify_church_numeral(fst))
            return handle_rest

        def handle_nil(_):
            pass

        closure(handle_first)(handle_nil)

    helper(exp)
    return res

def eval_lambda_exp(s):
    return LambdaParser(s).parse().eval({})

def natify_bool(exp):
    return exp(lambda _: True)(lambda _: False)

def if_expr(cond_exp, then_exp, else_exp):
    return f'{cond_exp}(lambda _: {then_exp})(lambda _: {else_exp})'

def not_expr(exp):
    return if_expr(exp, false, true)

def and_expr(exp1, exp2):
    return if_expr(exp1, exp2, false)

def or_expr(exp1, exp2):
    return if_expr(exp1, true, exp2)

def church_numeral(n):
    if n == 0:
        return '(lambda g: (lambda z: z))'
    return f'(lambda g: (lambda z: g({church_numeral(n-1)}(g)(z))))'

def natify_church_numeral(exp):
    return exp(lambda x: x+1)(0)

def add(exp1, exp2):
    return f'(lambda g: (lambda z: {exp1}(g)({exp2}(g)(z))))'

def less_than(a, b):
    return not_expr(is_zero(sub(b, a)))

def eq(a, b):
    return and_expr(is_zero(sub(a,b)),
                    is_zero(sub(b, a)))

def mul(exp1, exp2):
    return f'(lambda g: (lambda z: {exp1}(lambda x: {exp2}(g)(x))(z)))'

pred = '(lambda n : (lambda f: (lambda z: n(lambda g: lambda h: h(g(f)))(lambda u: z)(lambda u: u))))'

def sub(exp1, exp2):
    return f'{exp2}({pred})({exp1})'

YCombinator = '(lambda y: (lambda F: F(lambda x: y(y)(F)(x))))(lambda y: (lambda F: F(lambda x: y(y)(F)(x))))'


def let(name, value, body):
    return f'(lambda {name}:{body})({value})'

def let_rec(fname, lam, body):
    return let(fname, f'{YCombinator}(lambda {fname}: {lam})', body)

def call(f, arg):
    return f'{f}({arg})'

def function(arg, body):
    return f'(lambda {arg}: {body})'

def multi_arg_function(args, body):
    if len(args) == 0:
        return f'(lambda _: {body})'
    return function(args[0], multi_arg_function(args[1:], body))

def multi_arg_call(f, args):
    res = f
    for arg in args:
        res = call(res, arg)
    res = call(res, void)
    return res

def int_list(lst):
    if len(lst) == 0:
        return nil
    return pair(church_numeral(lst[0]),
                int_list(lst[1:]))
