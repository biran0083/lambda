from lambda_expr import *
from collections import namedtuple

builtin_fun_map = {
    'is_nil': is_nil,
    'pair': pair,
    'first': first,
    'rest': rest,
}

class Prog(namedtuple('Prog', ['funcs'])):
    def helper(self, i):
        if len(self.funcs) == i:
            return multi_arg_call('main', [])
        f = self.funcs[i]
        return let_rec(f.fname, 
                       multi_arg_function(f.args, f.body.compile()),
                       self.helper(i + 1))

    def compile(self):
        return self.helper(0)

class Func(namedtuple('Func', ['fname', 'args', 'body'])):
    def compile(self):
        return multi_arg_function(self.args, self.body.compile())

class If(namedtuple('If', ['cond', 'then_expr', 'else_expr'])):
    def compile(self):
        return if_expr(self.cond.compile(),
                       self.then_expr.compile(),
                       self.else_expr.compile())

class Int(namedtuple('Int', ['value'])):
    def compile(self):
        return church_numeral(self.value)

class Bool(namedtuple('Bool', ['value'])):
    def compile(self):
        return true if self.value else false

class List(namedtuple('List', ['values'])):
    def helper(self, i):
        if i == len(self.values):
            return nil
        return pair(self.values[i].compile(), self.helper(i + 1))

    def compile(self):
        return self.helper(0)

class Call(namedtuple('Call', ['f', 'params'])):
    def compile(self):
        fun = self.f.compile() 
        params = [param.compile() for param in self.params]
        if fun in builtin_fun_map:
            return builtin_fun_map[fun](*params)
        return multi_arg_call(fun, params)

class Id(namedtuple('Id', ['name'])):
    def compile(self):
        return self.name

class BinaryOpExpr(namedtuple('BinaryOpExpr', ['op', 'exp1', 'exp2'])):
    def compile(self):
        op = {'+':add, '-':sub, '*':mul, '&&': and_expr, '||': or_expr,
              '==': eq, '<': less_than }[self.op]
        return op(self.exp1.compile(), self.exp2.compile())

class UnaryOpExpr(namedtuple('UnaryOpExpr', ['op', 'exp'])):
    def compile(self):
        return {'not': not_expr}[self.op](self.exp.compile())
    
class Let(namedtuple('Let', ['id', 'exp'])):
    pass

class Stmts(namedtuple('Stmts', ['lets', 'exp'])):
    def helper(self, i):
        if i == len(self.lets):
            return self.exp.compile()
        return let(self.lets[i].id, self.lets[i].exp.compile(), self.helper(i+1))

    def compile(self):
        return self.helper(0)
