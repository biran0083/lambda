# lambda
Prove lambda expression is Turing complete by compiling high level language into lambda expression.

# Tools
**hl3_compiler.py** Compile high level language hl3 (High Level Language for Lambda) into lambda expression.

**lambda_interpreter.py** python lambda expression interpreter. Python interpreter could evaluate the lambda expression as well, but occassionally run into MemoryError due to deeply nested calls.

# hl3 
A simple high level Turing complete language.
## Syntax
```
    prog  : funcs
    funcs : func
    funcs : funcs func
    func  : "fn" ID ( args ) { stmts }
    stmts : expr
          | lets expr
    lets  : let
          | lets let
    let   : "let" ID = expr ;
    expr  : []
          | [ expr_list ]
          | int-literals
          | bool-literals
          | ID
          | "if" expr { stmts } "else" { stmts }
          | expr ( expr_list )
          | ( expr )
          | expr + expr
          | expr - expr
          | expr * expr
          | expr && expr
          | expr || expr
          | expr == expr
          | expr < expr
          | ! expr 
```
## Built-in functions
- pair: construct a pair
- firtst: get first element of the pair
- rest: get second element of the pair
- is_nil: if list is empty
- print_int: print int value
- print_bool: print bool value
- print_int_list: print int list

# References
- Parser is built on top of [ply](https://github.com/dabeaz/ply).
- Ideal borrowed from Matt Might's [fantastic blog post](https://matt.might.net/articles/compiling-up-to-lambda-calculus/).
