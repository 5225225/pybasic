import sys
import string
import pickle
import util



linenum = 1



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
        tokens.append(util.token("NUMBER", currword, linenum))

    elif currword in OPERATORS:
        while True:
            ch = getchar()
            if not ch:
                break
            if ch not in "".join(OPERATORS):
                pushchar(ch)
                break
            currword += ch
        tokens.append(util.token("OPERATOR", currword, linenum))

    elif currword == '"': 
        ending = currword
        while True:
            ch = getchar()
            if not ch:
                break
            currword += ch
            if ch == ending:
                break
        tokens.append(util.token("STRING", currword[1:-1], linenum))

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
                tokens.append(util.token("KEYWORD", currword, linenum))
            else:
                tokens.append(util.token("VARIABLE", currword, linenum))
    elif currword == "'":
        while True:
            ch = getchar()
            if ch == "\n":
                break

    elif currword == "\n":
        tokens.append(util.token("EOC", "NEWLINE", linenum))

    elif currword == "(":
        tokens.append(util.token("PAREN", "(", linenum))

    elif currword == ")":
        tokens.append(util.token("PAREN", ")", linenum))

    elif currword == ":":
        while True:
            ch = getchar()
            if not(ch in string.ascii_letters):
                pushchar(ch)
                break
            currword += ch
        tokens.append(util.token("LABEL", currword[1:], linenum))
    elif currword == ",":
        tokens.append(util.token("DELIM", ",", linenum))


sys.stdout.buffer.write(pickle.dumps(tokens))
