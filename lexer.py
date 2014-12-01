from defs import TokenType 
import string

class SymbolEntry:
    def __init__(self, TokenType, value, line):
        self.line = line
        self.kind = TokenType
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
        if not self.eof:
            char = self._get_current_line()[self.pos]
        return char 

    def _get_current_line(self):
        return self.lines[self.cur_line]

    def next_char(self):
        if len(self.lines) == 0:
            raise Exception("No lines")

        if self.pos >= len(self._get_current_line()):
            line = self.fd.readline()
            if line is "":
                self.eof = True
                return None
            line = line.rstrip("\n")
            self.lines.append(line)
            self.pos = 0
        char = self.get_char()
        self.pos += 1
        if self.pos >= len(self._get_current_line()):
            line = self.fd.readline()
            if line is "":
                self.eof = True
                return None
            line = line.rstrip("\n")
            self.lines.append(line)
            self.cur_line += 1
            self.pos = 0
        return char 

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

    def __init__(self, filename):
        self.line = None
        self.inp = None
        self.stable = [ ]
        self.stream = FileStream(filename)
        
    def read_letters(self):
        id = ""
        self.stream.put_char()
        while(True):
            char = self.stream.next_char()
            if char is not None and char in string.ascii_letters:
                id += char
            else:
                self.stream.put_char()
                break
        return id

    def get_token(self):
        global line_num
        while(True):
            char = self.stream.next_char()
            if not char:
                return None
            if char is "(":
                self.stable.append(SymbolEntry(TokenType.LPAREN, "(", self.stream.current_line_num()))
            if char is ")":
                self.stable.append(SymbolEntry(TokenType.RPAREN, ")", self.stream.current_line_num()))
            elif char in string.ascii_letters:
                return self.read_letters()
            elif char in string.whitespace:
                pass
            elif char in string.punctuation:
                return char 
            else:
                return "UNKNOWN: " + char

    def print_stable(self):
        for entry in self.stable:
            print "Kind: {0}, Value : {1}, Line: {2}".format(TokenType.map_kind_to_str(entry.kind), entry.val, entry.line)

