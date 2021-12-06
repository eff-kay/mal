from posixpath import islink
import re

_s2u = lambda x:x
_u = lambda x: x

class Symbol(str): pass
def _symbol(str): return Symbol(str)

class Keyword(str): pass
def _keyword(str): return Keyword(str)

class Vector(list):
    pass

class HashMap(dict):
    pass

def _read_hashmap(values):
    hm = HashMap()
    print('valeues', values)
    for i in range(0, len(values[:-1]), 2):
        hm[values[i]] = values[i+1]
    print('hm', hm)
    return hm

def read_hashmap(reader):
    lst = read_sequence(reader, list, '{', '}')
    return _read_hashmap(lst)

def read_list(reader):
    return read_sequence(reader, seq_type=list, start="(", end=")")

def read_vector(reader):
    return read_sequence(reader, seq_type=Vector, start="[", end="]")

def read_sequence(reader, seq_type=list, start='(', end=')'):
    results = seq_type()
    error = False

    # print('read list', reader.position, reader.tokens)
    token = reader.next()

    if token != start:
        raise Exception("not starting correctly")

    token = reader.peek()
    while token != end:
        if not token: 
            raise Exception("expected ')' got EOF")
        value = read_form(reader)
        results.append(value)
        token = reader.peek()

    # print('before returning', reader.position, reader.tokens)
    reader.next()
    return results

def _unescape(s):
    return s.replace('\\"', '"').replace("\\n", "\n")

def read_atom(reader):
    token = reader.next()
    int_re = re.compile(r"-?[0-9]+$")
    float_re = re.compile(r"-?[0-9][0-9.]*$")
    string_re = re.compile(r'"(?:[\\].|[^\\"])*"')


    if re.match(int_re, token):
        value = int(token)
    elif re.match(float_re, token):
        value = int(token)
    elif re.match(string_re, token):
        value = _unescape(token[1:-1])
    elif token[0] == '"':           raise Exception("expected '\"', got EOF")
    elif token[0] == ":":
        value = _keyword(token)
    # elif token == "nil":            return None
    # elif token == "true":           return True
    # elif token == "false":          return False
    # elif re.match(string_re, token):
    #     print('token', token)
    #     unesc = _unescape(token[1:-1])
    #     value = _s2u(unesc)
    #     print('values', value, 'token', token, 'unesc', unesc)

    else:
        value = _symbol(token)

    # print('read_atom: token, ', token, 'value, ', value)
    return value

def read_form(reader):
    # return mal datatype->ast
    # list of mal-types
    token = reader.peek()
    if token == '\'':
        reader.next()
        return [_symbol('quote'), read_form(reader)]
    elif token == '`':
        reader.next()
        return [_symbol('quasiquote'), read_form(reader)]
    elif token == '~':
        reader.next()
        return [_symbol('unquote'), read_form(reader)]
    elif token == '~@':
        reader.next()
        return [_symbol('splice-unquote'), read_form(reader)]
    elif token == '@':
        reader.next()
        return [_symbol('deref'), read_form(reader)]
    
    elif token=="^":
        return_list = [_symbol('with-meta')]
        reader.next()
        meta = read_form(reader)
        meta_list = read_form(reader)

        return_list.append(meta_list)
        return_list.append(meta)

        return return_list

    elif token=="(":
        # token = reader.next()
        values = read_list(reader)
        # print('valeus', values)
        return values
    elif token=='[':
        values = read_vector(reader)
        return values
    elif token=='{':
        values = read_hashmap(reader)
        return values
    else:
        value = read_atom(reader)
        return value


def tokenize(str_input:str):
    # tokens = re.findall(r"""[\s,]*(~@|[\[\]{}()'`~^@]|"(?:[\\].|[^\\"])*"?|;.*|[^\s\[\]{}()'"`,;]+)""", str_input)
    # tre = re.compile(r"""[\s,]*(~@|[\[\]{}()'`~^@]|"(?:[\\].|[^\\"])*"?|;.*|[^\s\[\]{}()'"`@,;]+)""");
    # tokens = [t for t in tokens if t[0] != ';']
    # print("tokens read", tokens)
    # return tokens
    tre = re.compile(r"""[\s,]*(~@|[\[\]{}()'`~^@]|"(?:[\\].|[^\\"])*"?|;.*|[^\s\[\]{}()'"`@,;]+)""");
    tokens = [t for t in re.findall(tre, str_input) if t[0] != ';']

    print('tokens ', tokens)
    return tokens

def read_str(str):
    tokens = tokenize(str)
    reader = Reader(tokens)

    tokens = read_form(reader)
    # print('retun tokens ', tokens)
    return tokens


class Reader():
    tokens = []

    def __init__(self, tokens):
        self.tokens = tokens
        self.position = 0

    def next(self):
        token = self.tokens[self.position]
        self.position+=1
        return token

    def peek(self):
        # return token at current position
        if len(self.tokens) > self.position:
            return self.tokens[self.position]
        else:
            return None