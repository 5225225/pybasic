import sys


class token:
    def __init__(self, tokentype, value):
        self.tokentype = tokentype
        self.value = value

    def __repr__(self):
        return "token({}, {})".format(self.tokentype, self.value)

class ast_node:
    def __init__(self, token, children=[]):
        self.token = token
        self.children = children

    def __repr__(self):
        return "({}) {}".format(self.token, self.children)

def parse_exp(exp):
    return ast_node(token("STRING", "TEST"))


tokens = []
ast = []

for line in sys.stdin.readlines():
    ttype, val = line.strip().split("|")
    tokens.append(token(ttype, val))

t = tokens[:]
assert t is not tokens


while t != []:
    currt = t.pop(0)

    if currt.tokentype == "KEYWORD":
        if currt.value == "PRINT":
            toprint = t.pop(0)
            if toprint.tokentype == "STRING":
                node = ast_node(currt, [toprint])
                ast.append(node)
            else:
                exp = [toprint]
                while True:
                    x = t.pop(0)
                    if x.tokentype in ["NUMBER", "OPERATOR", "VARIABLE"]:
                        exp.append(x)
                    elif x.tokentype == "EOC":
                        break
                    else:
                        print("Unexpected token in PRINT statement")
                        sys.exit(1)
                parsed = parse_exp(exp)
                ast.append(parsed)
    else:
        pass

for x in ast:
    print(x)
