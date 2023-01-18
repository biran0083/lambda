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
    
