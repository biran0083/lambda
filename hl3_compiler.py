#!python3
from hl3_parser import parse
import sys

def main():
    exp = sys.stdin.read()
    print(parse(exp).compile())

if __name__ == '__main__':
    main()
