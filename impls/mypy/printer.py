
# from reader import Symbol

def pr_str(tokens):
    str_out = ''

    if isinstance(tokens, int):
        str_out += str(tokens)
    elif isinstance(tokens, list):
        str_temp = '('
        for j, t in enumerate(tokens):
            str_temp += pr_str(t)
            if j!=len(tokens)-1:
                str_temp+=' '
        str_temp += ')'
        str_out += str_temp
    else:
        str_out+=tokens

    # print('str_out', str_out)
    return str_out