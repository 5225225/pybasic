import sys
import pickle
import util


def pptokens(tokens):
    return " ".join([x.value for x in tokens])

def parse_exp(exp):
    stack = []
    for token in exp:
        if token.tokentype in ["NUMBER", "VARIABLE"]:
            stack.append(token)
        if token.tokentype == "OPERATOR":
            arg1, arg2 = stack.pop(), stack.pop()
            node = util.ast_node(token, [arg1, arg2])
            stack.append(node)
    return stack

order = {
    "+": 1,
    "-": 1,
    "*": 2,
    "/": 2,
}

def print_tree(x, indent=0):
    if type(x) is token:
        print(" "*indent + x.value)
    else:
        print(" "*indent + x.token.value)
        for item in x.children:
            print_tree(item, indent+1)

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
                try:
                    while not(stack[-1].value == "("):
                        output.append(stack.pop())
                except ValueError:
                    print("Syntax error, mismatched parenthesis")
                    print("No idea what line it's on!")
                    sys.exit(1)
                stack.pop()


        if len(tokens) == 0:
            break

    while len(stack) != 0:
        output.append(stack.pop())
        
    return output
tokens = []
ast = []

tokens = pickle.loads(sys.stdin.buffer.read())

t = tokens[:]
assert t is not tokens


while t != []:
    currt = t.pop(0)

    if currt.tokentype == "KEYWORD":
        if currt.value == "PRINT":
            toprint = t.pop(0)
            if toprint.tokentype == "STRING":
                node = util.ast_node(currt, [util.ast_node(toprint)])
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
                x = infix_to_postfix(exp)
                parsed = parse_exp(x)
                ast.append(util.ast_node(currt, parsed))
                # No idea WHY it needs a [0], TODO figure it out
    else:
        pass


sys.stdout.buffer.write(pickle.dumps(ast))
