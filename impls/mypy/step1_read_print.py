import sys, traceback
import mal_readline
import reader
import printer

# read
def READ(str):
    return reader.read_str(str)

# eval
def EVAL(ast, env):
        return ast

# print
def PRINT(exp):
    return printer.pr_str(exp)

# repl
def REP(str):
    return PRINT(EVAL(READ(str), {}))

# repl loop
while True:
    try:
        line = mal_readline.readline("user> ")
        if line == None: break
        if line == "": continue
        print(REP(line))
    except Exception as e:
        print("".join(traceback.format_exception(*sys.exc_info())))