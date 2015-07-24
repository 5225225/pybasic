import sys
import string
import json

linenum = 1

class token:
    def __init__(self, tokentype, value):
        self.tokentype = tokentype
        self.value = value
        self.linenum = linenum
        # Valid tokentypes

        # KEYWORD
        # STRING
        # NUMBER
        # VARIABLE
        # OPERATOR
        # LABEL
        # PAREN
        # EOC

    def __repr__(self):
        return "token({}, {}) line:{}".format(self.tokentype,
        self.value, self.linenum)

def getchar():
    global holdchr
    global linenum
    if holdchr is None:
        ch = sys.stdin.read(1)
        if ch == "\n":
            linenum += 1
        return ch
    else:
        toret = holdchr
        holdchr = None
        return toret

def pushchar(ch):
    global holdchr
    if holdchr is not None:
        raise ValueError
    else:
        holdchr = ch

    

KEYWORDS = [
    "PRINT",
    "LET",
    "THEN"
    "IF"
]

OPERATORS = [
    "+",
    "-",
    "*",
    "/",
    "=",
    "==",
]

tokens = []
holdchr = None

while True:
    currword = ""
    ch = getchar()
    if not ch:
        break
    currword += ch

    if ch in [str(x) for x in range(10)]:
        while True:
            ch = getchar()
            if not ch:
                break
            if ch not in [str(x) for x in range(10)]:
                pushchar(ch)
                break
            currword += ch
        tokens.append(token("NUMBER", currword))

    elif currword in OPERATORS:
        while True:
            ch = getchar()
            if not ch:
                break
            if ch not in "".join(OPERATORS):
                pushchar(ch)
                break
            currword += ch
        tokens.append(token("OPERATOR", currword))

    elif currword == '"': 
        ending = currword
        while True:
            ch = getchar()
            if not ch:
                break
            currword += ch
            if ch == ending:
                break
        tokens.append(token("STRING", currword[1:-1]))

    elif currword in string.ascii_letters:
        # We don't know if this is going to be a variable name or a keyword
        while True:
            ch = getchar()
            if not ch:
                break
            if not(ch in string.ascii_letters + string.digits):
                pushchar(ch)
                break
            currword += ch

        if currword == "REM":
            while True:
                ch = getchar()
                if ch == "\n":
                    break
        else:
            if currword in KEYWORDS:
                tokens.append(token("KEYWORD", currword))
            else:
                tokens.append(token("VARIABLE", currword))
    elif currword == "'":
        while True:
            ch = getchar()
            if ch == "\n":
                break

    elif currword == "\n":
        tokens.append(token("EOC", "NEWLINE"))

    elif currword == "(":
        tokens.append(token("PAREN", "("))

    elif currword == ")":
        tokens.append(token("PAREN", ")"))

    elif currword == ":":
        while True:
            ch = getchar()
            if not(ch in string.ascii_letters):
                pushchar(ch)
                break
            currword += ch
        tokens.append(token("LABEL", currword[1:]))
    elif currword == ",":
        tokens.append(token("DELIM", ","))

    
for item in tokens: 
    print("{}|{}".format(item.tokentype, item.value))
