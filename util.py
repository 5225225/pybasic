class token:
    def __init__(self, tokentype, value, linenum):
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

class ast_node:
    def __init__(self, token, children=[]):
        self.token = token
        self.children = children

    def __repr__(self):
        return "ast_node({}, [{}])".format(self.token, self.children)
