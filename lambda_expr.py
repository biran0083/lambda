#!python3
from lambda_parser import LambdaParser

void = '(lambda x: x)'
true = f'(lambda true: (lambda false: true({void})))'
false = f'(lambda true: (lambda false: false({void})))'
nil = f'(lambda onPair: (lambda onNil: onNil({void})))'
YCombinator = '(lambda y: (lambda F: F(lambda x: y(y)(F)(x))))(lambda y: (lambda F: F(lambda x: y(y)(F)(x))))'

def print_int(exp):
    print(natify_church_numeral(exp))
    return eval(void)

def print_bool(exp):
    print(natify_bool(exp))
    return eval(void)

def print_int_list(exp):
    print(natify_int_list(exp))
    return eval(void)

def eval_lambda_exp(s):
    return LambdaParser(s).parse().eval({
        'print_int': print_int,
        'print_bool': print_bool,
        'print_int_list': print_int_list,
    })
                
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


def sub(exp1, exp2):
    pred = '(lambda n : (lambda f: (lambda z: n(lambda g: lambda h: h(g(f)))(lambda u: z)(lambda u: u))))'
    return f'{exp2}({pred})({exp1})'


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
