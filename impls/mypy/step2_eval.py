import sys, traceback
import mal_readline
import reader
import printer

from reader import HashMap, Symbol, Vector


repl_env = {
    '+': lambda a, b:a+b, 
    '-': lambda a, b:a-b,
    '*': lambda a, b:a*b,
    '/': lambda a, b:a//b
}

def eval_ast(ast, env):
    if type(ast)==list:
        return [EVAL(x, env) for x in ast]
    elif type(ast)==Vector:
        vector = [EVAL(x, env) for x in ast]
        return Vector(vector)
    elif type(ast)==HashMap:
        new_hm = {EVAL(k, env):EVAL(v, env) for k,v in ast.items()}
        return HashMap(new_hm)

    elif type(ast)==Symbol:
        return env[ast]
    else:
        return ast

# read
def READ(str):
    return reader.read_str(str)

# eval
def EVAL(ast, env):
        if type(ast)==list:
            if len(ast)==0:
                return ast
            print('list ', ast)
            new_list = eval_ast(ast, env)
            return new_list[0](*new_list[1:])
        else:
            print('not list', ast)
            return eval_ast(ast, env)

# print
def PRINT(exp):
    return printer.pr_str(exp)

# repl
def REP(str):
    return PRINT(EVAL(READ(str), repl_env))

# repl loop
while True:
    try:
        line = mal_readline.readline("user> ")
        if line == None: break
        if line == "": continue
        print(REP(line))
    except Exception as e:
        print("".join(traceback.format_exception(*sys.exc_info())))