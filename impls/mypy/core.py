
def eq(x, y):
    if type(x)==type(y):
        if isinstance(x, list):
            return all([i==j for i,j in zip(x,y)])
        else:
            return x==y

def ret_list(x=None):
    return list(x) if x else []

ns = {
    '+': lambda a, b:a+b, 
    '-': lambda a, b:a-b,
    '*': lambda a, b:a*b,
    '/': lambda a, b:a//b,
    'list': ret_list, 
    'list?': lambda x: type(x)==list,
    'empty?': lambda x: len(x)==0,
    'count': lambda x: len(x),
    '=': eq,
    '<':lambda x,y:x<y,
    '<=': lambda x,y:x<=y,
    '>': lambda x,y:x>y,
    '>=':lambda x,y:x>=y
}


