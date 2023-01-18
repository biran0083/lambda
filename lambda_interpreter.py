#!python3
from lambda_expr import eval_lambda_exp
import sys

def main():
    sys.setrecursionlimit(1000000)
    exp = input()
    eval_lambda_exp(exp)

if __name__ == '__main__':
    main()
