#!python3
import string
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
