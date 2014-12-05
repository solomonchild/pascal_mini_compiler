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
        return "Kind: {0}, value: \"{1}\", idx: {2}".format(self.kind, self.val, self.idx)

class IDEntry:
    def __str__(self):
            return "Identifier({0}), value: \"{1}\"".format(self.kind, self.val)

    def __init__(self, kind, value):
        self.kind = TokenType.ID
        self.val = value

class LiteralEntry:
    def __str__(self):
            return "Literal ({0}), value: \"{1}\"".format(self.kind, self.val)

    def __init__(self, kind, value):
        self.kind = kind
        self.val = value

class KeywordTableEntry:
    def __init__(self, val, kind, isSep = False):
        self.val = val
        self.kind = kind
        self.isSep = isSep

    def __str__(self):
        return "Keyword ({0}), value: \"{1}\", is a separator: {2}".format(self.kind, self.val, self.isSep)

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

    def getChar(self):
        char = None
        #if len(self.lines) == 0:
            #raise Exception("No lines")
        if self.pos == len(self._get_current_line()) - 1 and self.cur_line == len(self.lines) - 1 and self.eof:
            return None

        char = self._get_current_line()[self.pos]
        self.pos += 1

        if self.pos >= len(self._get_current_line()):
            if self.cur_line == len(self.lines) -1:
                line = self.fd.readline()
                if line is "":
                    self.eof = True
                line = line.rstrip("\n")
                if line is not "":
                    self.lines.append(line)
            self.pos = 0
            self.cur_line += 1

        return char 

    def _get_current_line(self):
        return self.lines[self.cur_line]

    def putChar(self, how_many = 1):
        while how_many > 0:
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
            how_many -= 1
        

    

class Lexer:

    
    def __init__(self, stream):
        self.line = None
        self.inp = None
        self.sym_table = [ ]
        self.stream = stream
        self.lexeme = ""
        self.char = None
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
                KeywordTableEntry("(", TokenType.LPAREN, True),
                KeywordTableEntry(")", TokenType.RPAREN, True),
                KeywordTableEntry("[", TokenType.LSQUARE, True),
                KeywordTableEntry("]", TokenType.RSQUARE, True),
                KeywordTableEntry(",", TokenType.COMMA, True),
                KeywordTableEntry(".", TokenType.DOT, True),
                KeywordTableEntry(";", TokenType.SEMICOLON, True),
                KeywordTableEntry(":", TokenType.COLON, True),
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
        self.getChar()
        while self.char and (self.char in string.ascii_letters or self.char in string.digits):
                self.lexeme += self.char
                self.getChar()
        self.putChar()

    def processLexeme(self, kind = TokenType.ID):
        if kind is TokenType.ID:
            kwIndex = self.getIndexOfKw(self.lexeme)
            #first check if exists in the keyword table
            if kwIndex is not None:
                kwEntry = self.keywords[kwIndex]
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

    def getChar(self):
        self.char = self.stream.getChar()

    def putChar(self, howMany = 1):
        self.stream.putChar(howMany)

    def get_token(self):
        global line_num
        while True:
            self.lexeme = ""
            self.getChar()

            if not self.char:
                return None

            if self.char in string.whitespace:
                while self.char and self.char in string.whitespace:
                    self.getChar()
                if self.char:
                    self.putChar()
                continue
            elif self.char is "\"" or self.char is "\'":
                op_quote = self.char
                self.getChar()
                escape = self.char is "\\"
                while self.char and (escape or self.char is not op_quote):
                    escape = self.char is "\\"
                    if not escape:
                        self.lexeme += self.char
                    self.getChar()
                return self.processLexeme(TokenType.STRING)
            elif self.isId(self.char):
                self.putChar()
                self.readId()
                return self.processLexeme(TokenType.ID)

            elif self.char is "-" or self.char is "+":
                self.lexeme += self.char
                self.getChar()
                if self.char in string.digits:
                    while self.char and self.char in string.digits or (self.char is "." and "." not in self.lexeme):
                            self.lexeme += self.char
                            self.getChar()
                    self.putChar()
                    if "." in self.lexeme:
                        return self.processLexeme(TokenType.REAL)
                    return self.processLexeme(TokenType.INTEGER)
                else:
                    self.putChar(2)
                    self.getChar()
                    self.lexeme = "" 
            elif self.char in string.digits:
                    while self.char and self.char in string.digits or (self.char is "." and "." not in self.lexeme):
                            self.lexeme += self.char
                            self.getChar()
                    self.putChar()
                    if "." in self.lexeme:
                        return self.processLexeme(TokenType.REAL)
                    return self.processLexeme(TokenType.INTEGER)
            elif self.char is ":" or self.char is "<" or self.char is ">" or self.char is "=":
                self.lexeme += self.char
                self.getChar()
                if self.char is "=":
                    self.lexeme += self.char
                    return self.processLexeme()
                elif self.char is ">":
                    self.lexeme += self.char
                    return self.processLexeme()
                else:
                    self.putChar()
                    return self.processLexeme()
            if self.getIndexOfKw(self.char) is not None:
                self.lexeme += self.char
                return self.processLexeme()
            else:
                while self.char and self.char not in string.digits and self.char not in string.ascii_letters:
                    self.lexeme += self.char
                    self.getChar()
                self.putChar()
                return Token(TokenType.UNKNOWN, self.lexeme, 0, None)

    def printTable(self, table):
        i = 0
        for entry in table:
            print("{0}) {1}".format(i, entry))
            i += 1
