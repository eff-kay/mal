import sys, traceback
from env import ENV
import mal_readline
import reader
import printer

from reader import HashMap, Symbol, Vector
from core import ns as namespace

repl_env = ENV()

for sym, func in namespace.items():
    repl_env.set(sym, func)

def eval_ast(ast, env:ENV):
    if type(ast)==list:
        return [EVAL(x, env) for x in ast]
    elif type(ast)==Vector:
        vector = [EVAL(x, env) for x in ast]
        return Vector(vector)
    elif type(ast)==HashMap:
        new_hm = {EVAL(k, env):EVAL(v, env) for k,v in ast.items()}
        return HashMap(new_hm)
    elif type(ast)==Symbol:
        return env.get(ast)
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

            if ast[0]=='def!':
                return env.set(ast[1], EVAL(ast[2], env))
            elif ast[0]=='let*':
                a1, a2 = ast[1], ast[2]
                new_env = ENV(env)
                for i in range(0, len(a1), 2):
                    new_env.set(a1[i], EVAL(a1[i+1], new_env))
                res = EVAL(ast[2], new_env)
                return res
            elif ast[0]=='do':
                res = eval_ast(ast[1:], env)
                return res[-1]
            elif ast[0]=='if':
                res = eval_ast(ast[1], env)
                if res:
                    sec = eval_ast(ast[2], env)
                    return sec
                else:
                    third = eval_ast(ast[3], env) if len(ast)>3 else None
                    return third
            elif ast[0] == "fn*":
                def func(*params):
                    new_env = ENV(outer=env,  binds=ast[1], exprs=list(params))
                    res = EVAL(ast[2], new_env)
                    return res
                return func
            else:
                new_list = eval_ast(ast, env)
                return new_list[0](*new_list[1:])
        else:
            print('not list', ast)
            res_eval = eval_ast(ast, env)
            print('res not list', res_eval)
            return res_eval

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

