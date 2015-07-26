import sys
import pickle
import util

def eval_exp(tree_head):
    assert tree_head.token.tokentype == "OPERATOR"
    assert len(tree_head.children) == 2


if len(sys.argv) > 1:
    ast = pickle.load(open(sys.argv[1], "rb"))
else:
    ast = pickle.loads(sys.stdin.buffer.read())

assert type(ast) == list

linenum = 1

variables = {}
print(ast)

while True:
    try:
        currline = ast[linenum-1]
    except IndexError:
        break

    # I don't know why it doesn't work
    if currline.token.value == "PRINT":
        if currline.children[0].token.tokentype == "STRING":
            print(currline.children[0].token.value)
        
        else:
            raise NotImplementedError
    elif currline.token.value == "LET":
        pass
    else:
        raise NotImplementedError
    linenum += 1
