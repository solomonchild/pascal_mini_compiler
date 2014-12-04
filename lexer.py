import string
from enum import Enum

TokenType = Enum("TokenType", "LPAREN RPAREN IF AND OR THEN COMMA ID DOT COLON SEMICOLON PROCEDURE VAR BEGIN END ASSIGN OPERATOR WS LITERAL INTEGER REAL LSQUARE RSQUARE UNKNOWN")



class Token:
    def __init__(self, kind, val):
        self.kind = kind
        self.val = val

    def __str__(self):
        return "Kind: {0}, value: [{1}]".format(self.kind, self.val)

class SymbolEntry:

    def __str__(self):
            return "Kind: {0}, value: \"{1}\", line: {2}".format(self.kind, self.val, self.line)

    def __init__(self, Token, value, line):
        self.line = line
        self.kind = Token
        self.val = value

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
        self.keywords = {
                ":=" : TokenType.ASSIGN,
                "==" : TokenType.OPERATOR,
                ">=" : TokenType.OPERATOR,
                "<=" : TokenType.OPERATOR,
                "<>" : TokenType.OPERATOR,
                "<" : TokenType.OPERATOR,
                ">" : TokenType.OPERATOR,
                "if" : TokenType.IF,
                "and" : TokenType.AND,
                "or" : TokenType.OR,
                "then" : TokenType.THEN,
                "procedure" : TokenType.PROCEDURE,
                "var" : TokenType.VAR,
                "begin" : TokenType.BEGIN,
                "end" : TokenType.END,
                "(" : TokenType.LPAREN,
                ")" : TokenType.RPAREN,
                "[" : TokenType.LSQUARE,
                "]" : TokenType.RSQUARE,
                "," : TokenType.COMMA,
                "." : TokenType.DOT,
                ";" : TokenType.SEMICOLON,
                ":" : TokenType.COLON,
                "+" : TokenType.OPERATOR,
                "-" : TokenType.OPERATOR,
                "\\" : TokenType.OPERATOR,
                "*" : TokenType.OPERATOR,
        }

    def isId(self, str):
        return (lambda s: s in string.ascii_letters)(str)

    def readId(self):
        char = self.stream.get_char()
        while char and (char in string.ascii_letters or char in string.digits):
                self.lexeme += char
                char = self.stream.get_char()
        self.stream.put_char()

    def makeToken(self, kind):
        if self.lexeme in self.keywords:
            return Token(self.keywords[self.lexeme], self.lexeme)
        else:
            se = SymbolEntry(TokenType.ID, self.lexeme, self.stream.current_line_num())
            self.sym_table.append(se)
            return Token(TokenType.ID, se)

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
                return Token(TokenType.LITERAL, self.lexeme)
            elif self.isId(char):
                self.stream.put_char()
                self.readId()
                return self.makeToken(TokenType.ID)

            elif char is "-" or char is "+":
                self.lexeme += char
                char = self.stream.get_char()
                if char in string.digits:
                    while char and char in string.digits or (char is "." and "." not in self.lexeme):
                            self.lexeme += char
                            char = self.stream.get_char()
                    self.stream.put_char()
                    if "." in self.lexeme:
                        return Token(TokenType.REAL, self.lexeme)
                    return Token(TokenType.INTEGER, self.lexeme)
                else:
                    self.stream.put_char()
                    self.lexeme = "" 
            elif char in string.digits:
                    while char and char in string.digits or (char is "." and "." not in self.lexeme):
                            self.lexeme += char
                            char = self.stream.get_char()
                    self.stream.put_char()
                    if "." in self.lexeme:
                        return Token(TokenType.REAL, self.lexeme)
                    return Token(TokenType.INTEGER, self.lexeme)
            elif char is ":" or char is "<" or char is ">" or char is "=":
                self.lexeme += char
                char = self.stream.get_char()
                if char is "=":
                    self.lexeme += char
                    return Token(self.keywords.get(self.lexeme, TokenType.UNKNOWN), self.lexeme)
                elif char is ">":
                    self.lexeme += char
                    return Token(self.keywords.get(self.lexeme, TokenType.UNKNOWN), self.lexeme)
                else:
                    self.stream.put_char()
                    return Token(self.keywords.get(self.lexeme, TokenType.UNKNOWN), self.lexeme)
            if char in self.keywords:
                self.lexeme += char
                return Token(self.keywords.get(self.lexeme, TokenType.UNKNOWN), self.lexeme)
            else:
                while char and char not in string.digits and char not in string.ascii_letters:
                    self.lexeme += char
                    char = self.stream.get_char()
                self.stream.put_char()
                return Token(TokenType.UNKNOWN, self.lexeme)

    def print_sym_table(self):
        for entry in self.sym_table:
            print(entry )

