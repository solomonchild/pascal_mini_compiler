import string
from enum import Enum

TokenType = Enum("TokenType", "LPAREN RPAREN IF AND OR THEN COMMA ID DOT COLON SEMICOLON PROCEDURE VAR BEGIN END ASSIGN OPERATOR WS STRING INTEGER REAL LSQUARE RSQUARE UNKNOWN")



class Token:
    def __init__(self, kind, val, index, table):
        self.kind = kind
        self.val = val
        self.idx = index
        self.table = table

    def __str__(self):
        return "Kind: {0}, value: {1}, idx: {2}".format(self.kind, self.val, self.idx)

class IDEntry:
    def __str__(self):
            return "Identifier({0}), value: \"{1}\"".format(self.kind, self.val)

    def __init__(self, kind, value):
        self.kind = TokenType.ID
        self.val = value

class LiteralEntry:
    def __str__(self):
            return "Literal({0}), value: \"{1}\", index of id table: {2}".format(self.kind, self.val, self.idx)

    def __init__(self, kind, value):
        self.kind = kind
        self.val = value

class KeywordTableEntry:
    def __init__(self, val, kind, isSep = False):
        self.val = val
        self.kind = kind
        self.isSep = isSep

class FileStream:
    def __init__(self, filename):
        self.fd = open(filename, "r")
        self.pos = 0
        self.lines = []
        self.lines.append(self.fd.readline())
        self.cur_line = 0
        self.eof = False

    def current_line_num(self):
        return self.cur_line + 1

    def get_char(self):
        char = None
        if len(self.lines) == 0:
            raise Exception("No lines")

        if not self.eof:
            char = self._get_current_line()[self.pos]

        self.pos += 1
        if self.pos >= len(self._get_current_line()):
            line = self.fd.readline()
            line = line.rstrip("\n")
            if line is "":
                self.eof = True
                return None
            self.lines.append(line)
            self.pos = 0
            self.cur_line += 1
        return char 

    def _get_current_line(self):
        return self.lines[self.cur_line]

    def put_char(self, how_many = 1):
        if self.lines is []:
            raise Exception("No lines")
        elif self.pos == 0 :
            if self.cur_line == 0:
                raise Exception("Cannot put char: zeroeth position within only line")
            else:
                self.cur_line -= 1
                self.pos = len(self._get_current_line()) - 1
        else:
            self.pos -= 1
        

    

class Lexer:

    
    def __init__(self, stream):
        self.line = None
        self.inp = None
        self.sym_table = [ ]
        self.stream = stream
        self.lexeme = ""
        self.keywords = [
                KeywordTableEntry(":=", TokenType.ASSIGN),
                KeywordTableEntry("==", TokenType.OPERATOR),
                KeywordTableEntry(">=", TokenType.OPERATOR),
                KeywordTableEntry("<=", TokenType.OPERATOR),
                KeywordTableEntry("<>", TokenType.OPERATOR),
                KeywordTableEntry("<", TokenType.OPERATOR),
                KeywordTableEntry(">", TokenType.OPERATOR),
                KeywordTableEntry("if", TokenType.IF),
                KeywordTableEntry("and", TokenType.AND),
                KeywordTableEntry("or", TokenType.OR),
                KeywordTableEntry("then", TokenType.THEN),
                KeywordTableEntry("procedure", TokenType.PROCEDURE),
                KeywordTableEntry("var", TokenType.VAR),
                KeywordTableEntry("begin", TokenType.BEGIN),
                KeywordTableEntry("end", TokenType.END),
                KeywordTableEntry("(", TokenType.LPAREN, False),
                KeywordTableEntry(")", TokenType.RPAREN, False),
                KeywordTableEntry("[", TokenType.LSQUARE, False),
                KeywordTableEntry("]", TokenType.RSQUARE, False),
                KeywordTableEntry(",", TokenType.COMMA, False),
                KeywordTableEntry(".", TokenType.DOT, False),
                KeywordTableEntry(";", TokenType.SEMICOLON, False),
                KeywordTableEntry(":", TokenType.COLON, False),
                KeywordTableEntry("+", TokenType.OPERATOR),
                KeywordTableEntry("-", TokenType.OPERATOR),
                KeywordTableEntry("\\", TokenType.OPERATOR),
                KeywordTableEntry("*", TokenType.OPERATOR),
        ]

        self.identifiers = [
        ]

        self.literals = [
        ]
    
    def getIndexOfKw(self, val):
        for i in range(len(self.keywords)):
            if self.keywords[i].val == val:
                return i
        return None

    def isId(self, str):
        return (lambda s: s in string.ascii_letters)(str)

    def readId(self):
        char = self.stream.get_char()
        while char and (char in string.ascii_letters or char in string.digits):
                self.lexeme += char
                char = self.stream.get_char()
        self.stream.put_char()

    def processLexeme(self, kind = TokenType.ID):
        if kind is TokenType.ID:
            kwIndex = self.getIndexOfKw(self.lexeme)
            #first check if exists in the keyword table
            if kwIndex is not None:
                kwEntry = self.keywords[kwIndex]
                if self.lexeme == ":=":
                return Token(kwEntry.kind, self.lexeme, kwIndex, self.keywords)
            else:
                #true ID, not a keyword
                entry = IDEntry(kind, self.lexeme)
                self.identifiers.append(entry)
                return Token(TokenType.ID, self.lexeme, self.identifiers.index(entry), self.identifiers)
        else:
            #literal
            entry = LiteralEntry(kind, self.lexeme)
            self.literals.append(entry)
            return Token(kind, self.lexeme, self.literals.index(entry), self.literals)

    def get_token(self):
        global line_num
        while True:
            self.lexeme = ""
            char = self.stream.get_char()

            if not char:
                return None

            if char in string.whitespace:
                while char and char in string.whitespace:
                    char = self.stream.get_char()
                if char:
                    self.stream.put_char()
                continue
            elif char is "\"" or char is "\'":
                op_quote = char
                char = self.stream.get_char()
                escape = char is "\\"
                while char and (escape or char is not op_quote):
                    escape = char is "\\"
                    if not escape:
                        self.lexeme += char
                    char = self.stream.get_char()
                return self.processLexeme(TokenType.STRING)
            elif self.isId(char):
                self.stream.put_char()
                self.readId()
                return self.processLexeme(TokenType.ID)

            elif char is "-" or char is "+":
                self.lexeme += char
                char = self.stream.get_char()
                if char in string.digits:
                    while char and char in string.digits or (char is "." and "." not in self.lexeme):
                            self.lexeme += char
                            char = self.stream.get_char()
                    self.stream.put_char()
                    if "." in self.lexeme:
                        return self.processLexeme(TokenType.REAL)
                    return self.processLexeme(TokenType.INTEGER)
                else:
                    self.stream.put_char()
                    self.lexeme = "" 
            elif char in string.digits:
                    while char and char in string.digits or (char is "." and "." not in self.lexeme):
                            self.lexeme += char
                            char = self.stream.get_char()
                    self.stream.put_char()
                    if "." in self.lexeme:
                        return self.processLexeme(TokenType.REAL)
                    return self.processLexeme(TokenType.INTEGER)
            elif char is ":" or char is "<" or char is ">" or char is "=":
                self.lexeme += char
                char = self.stream.get_char()
                if char is "=":
                    self.lexeme += char
                    return self.processLexeme()
                elif char is ">":
                    self.lexeme += char
                    return self.processLexeme()
                else:
                    self.stream.put_char()
                    return self.processLexeme()
            if self.getIndexOfKw(char):
                self.lexeme += char
                return self.processLexeme()
            else:
                while char and char not in string.digits and char not in string.ascii_letters:
                    self.lexeme += char
                    char = self.stream.get_char()
                self.stream.put_char()
                return Token(TokenType.UNKNOWN, self.lexeme, 0)

