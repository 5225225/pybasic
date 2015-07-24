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

def pptokens(tokens):
    return " ".join([x.value for x in tokens])

def parse_exp(exp):
    stack = []
    for token in exp:
        if token.tokentype in ["NUMBER", "VARIABLE"]:
            stack.append(token)
        if token.tokentype == "OPERATOR":
            arg1, arg2 = stack.pop(), stack.pop()
            node = ast_node(token, [arg1, arg2])
            stack.append(node)
    print(stack)

order = {
    "+": 1,
    "-": 1,
    "*": 2,
    "/": 2,
}

def infix_to_postfix(tokens):
    output = []
    stack = []

    while True:
        token = tokens.pop(0)
        if token.tokentype == "NUMBER":
            output.append(token)
        elif token.tokentype == "OPERATOR":
            if not(len(stack) == 0) and stack[-1].tokentype == "OPERATOR":
                if order[token.value] <= order[stack[-1].value]:
                    output.append(stack.pop())
            stack.append(token)

        elif token.tokentype == "PAREN":
            if token.value == "(":
                stack.append(token)

            else:
                if len(stack) == 0:
                    print("Syntax error, mismatched parenthesis")
                    print("No idea what line it's on!")
                    sys.exit(1)
                while not(stack[-1].value == "("):
                    output.append(stack.pop())
                stack.pop()


        if len(tokens) == 0:
            break

    while len(stack) != 0:
        output.append(stack.pop())
        
    return output
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
                    if x.tokentype in ["PAREN", "NUMBER", "OPERATOR", "VARIABLE"]:
                        exp.append(x)
                    elif x.tokentype == "EOC":
                        break
                    else:
                        print("Unexpected token in PRINT statement")
                        sys.exit(1)
                print(pptokens(exp))
                x = infix_to_postfix(exp)
                print(pptokens(x))
                parsed = parse_exp(x)
                print(parsed)
                ast.append(parsed)
    else:
        pass

