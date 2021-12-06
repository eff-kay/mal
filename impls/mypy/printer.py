
from reader import Keyword, Symbol,HashMap
from reader import Vector
def _escape(s):
    return s.replace('"', '\\"').replace('\n', '\\n')

def pr_str(tokens):
    str_out = ''

    print('printing tokens', tokens, type(tokens).__name__, str(type(tokens)))
    if isinstance(tokens, int):
        str_out += str(tokens)
    elif isinstance(tokens, Vector):
        str_temp = '['
        for j, t in enumerate(tokens):
            str_temp += pr_str(t)
            if j!=len(tokens)-1:
                str_temp+=' '
        str_temp += ']'
        str_out += str_temp
    elif isinstance(tokens, list):
        str_temp = '('
        for j, t in enumerate(tokens):
            str_temp += pr_str(t)
            if j!=len(tokens)-1:
                str_temp+=' '
        str_temp += ')'
        str_out += str_temp
    elif isinstance(tokens, HashMap):
        str_temp = '{'
        for i, (k, v) in enumerate(tokens.items()):
            str_temp += pr_str(k) + " " + pr_str(v)
            if i!=len(tokens)-1:
                str_temp+=' '
        str_temp += '}'
        str_out += str_temp
    elif isinstance(tokens, Symbol):
        str_out+= str(tokens)
    elif isinstance(tokens, Keyword):
        str_out+=str(tokens)
    elif isinstance(tokens, str):
        str_out+='"' + _escape(tokens) + '"'
    elif type(tokens).__name__=='function':
        str_out+="#<function"
    else:
        print('stirng', tokens)
        str_out+=tokens

    # print('str_out', str_out)
    return str_out