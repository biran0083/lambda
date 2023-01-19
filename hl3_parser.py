#!python3
from ply import lex, yacc
from hl3_ast import *

reserved = ('IF', 'FN', 'LET', 'ELSE')

tokens = ('LT', 'AND', 'OR', 'NOT', 'ADD', 'SUB', 'MUL', 'EQ', 'ASSIGN', 'SEMICOLON', 'COMMA', 'LPAREN', 'RPAREN', 'LBRACE', 'RBRACE', 'ID', 'INT', 'BOOL', 'LBRACKET', 'RBRACKET') + reserved

t_LT = '<'
t_AND = '&&'
t_OR = r'\|\|'
t_NOT = '!'
t_ADD = r'\+'
t_SUB = '-'
t_MUL = r'\*'
t_EQ = '=='
t_ASSIGN = '='
t_SEMICOLON = ';'
t_INT = r'\d+'
t_BOOL = 'true|false'
t_LBRACKET = r'\['
t_RBRACKET = r'\]'
t_COMMA = ','
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LBRACE = '{'
t_RBRACE = '}'
t_ignore = ' \t\n\r'
reserved_map = { k.lower() : k  for k in reserved }

def t_ID(t):
    r'[_a-zA-Z][\w_]*'
    if t.value in reserved_map:
        t.type = reserved_map[t.value]
    return t

def t_error(t):
    print(f'Illegal character {t.value[0]!r}')
    t.lexer.skip(1)

def p_prog(p):
    """
    prog : funcs
    """
    p[0] = Prog(p[1])

def p_list_empty(p):
    """
    expr0 : LBRACKET RBRACKET
    """
    p[0] = List([])

def p_list(p):
    """
    expr0 : LBRACKET expr_list RBRACKET
    """
    p[0] = List(p[2])

def p_funcs_base(p):
    """
    funcs : func
    """
    p[0] = [p[1]]

def p_funcs(p):
    """
    funcs : funcs func
    """
    p[0] = p[1] + [p[2]]

def p_func(p):
    """
    func : FN ID LPAREN args RPAREN LBRACE stmts RBRACE
    """
    p[0] = Func(p[2], p[4], p[7])

def p_func_no_arg(p):
    """
    func : FN ID LPAREN RPAREN LBRACE stmts RBRACE
    """
    p[0] = Func(p[2], [], p[6])

def p_int_expr(p):
    """
    expr0 : INT
    """
    p[0] = Int(int(p[1]))

def p_bool(p):
    """
    expr0 : BOOL
    """
    p[0] = Bool(p[1])

def p_if_expr(p):
    """
    expr0 : IF expr LBRACE stmts RBRACE ELSE LBRACE stmts RBRACE
    """
    p[0] = If(p[2], p[4], p[8])

def p_call_expr(p):
    """
    expr0 : expr0 LPAREN expr_list RPAREN
    """
    p[0] = Call(p[1], p[3])

def p_call_no_arg_expr(p):
    """
    expr0 : expr0 LPAREN RPAREN
    """
    p[0] = Call(p[1], [])

def p_stmts_simple(p):
    """
    stmts : expr
    """
    p[0] = Stmts([], p[1])

def p_stmts(p):
    """
    stmts : lets expr
    """
    p[0] = Stmts(p[1], p[2])

def p_lets(p):
    """
    lets : lets let
    """
    p[0] = p[1] + [p[2]]

def p_lets_one(p):
    """
    lets : let
    """
    p[0] = [p[1]]

def p_let(p):
    """
    let : LET ID ASSIGN expr SEMICOLON
    """
    p[0] = Let(p[2], p[4])

def p_expr_list_one(p):
    """
    expr_list : expr
    """
    p[0] = [p[1]]

def p_expr_list(p):
    """
    expr_list : expr_list COMMA expr
    """
    p[0] = p[1] + [p[3]]

def p_id_expr(p):
    """
    expr0 : ID
    """
    p[0] = Id(p[1])

def p_args_one(p):
    """
    args : ID 
    """
    p[0] = [p[1]]

def p_args(p):
    """
    args : args COMMA ID
    """
    p[0] = p[1] + [p[3]]

def p_binary_op_expr(p):
    """
    expr2 : expr2 ADD expr1
          | expr2 SUB expr1
          | expr2 AND expr1
          | expr2 OR expr1
          | expr2 EQ expr1
          | expr2 LT expr1
    """
    p[0] = BinaryOpExpr(p[2], p[1], p[3]) 

def p_mul(p):
    """
    expr1 : expr1 MUL expr0
    """
    p[0] = BinaryOpExpr(p[2], p[1], p[3]) 

def p_unary_op_expr(p):
    """
    expr0 : NOT expr0
    """
    p[0] = UnaryOpExpr(p[1], p[2])

def p_paren_expr(p):
    """
    expr0 : LPAREN expr RPAREN
    """
    p[0] = p[2]

def p_expr(p):
    """
    expr : expr2
    """
    p[0] = p[1]

def p_expr2(p):
    """
    expr2 : expr1
    """
    p[0] = p[1]

def p_expr1(p):
    """
    expr1 : expr0
    """
    p[0] = p[1]

def p_error(p):
    print(f'Syntax error at {p.value!r}')

def parse(s):
    lexer = lex.lex()
    parser = yacc.yacc()
    return parser.parse(s)

if __name__ == '__main__':
    import sys
    print(parse(sys.stdin.read())),
