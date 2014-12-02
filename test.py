import unittest
from lexer import *

class StubIo():
    def __init__(self, str):
        self.str = str
        self.pos = 0
        self.line_num = 0

    def current_line_num(self):
        return self.line_num + 1

    def readline(self):
        #le codeur
        if self.line_num > 0:
            return ""

        self.line_num = (lambda i: -~i)(self.line_num)
        return self.str

    def put_char(self):
        self.pos -= 1

    def get_char(self):
        if self.pos >= len(self.str):
            return None
        char = self.str[self.pos]
        self.pos += 1 
        return char



class LexerTest(unittest.TestCase):

    def setup(self):
        pass

    def teardown(self):
        pass
    
    def test_keyword(self):
        lexer = Lexer(StubIo("var"))
        token = lexer.get_token()
        self.assertTrue(isinstance(token, Token))
        self.assertEqual(token.kind, TokenType.VAR)
        self.assertEqual(token.val, "var")

    def test_id(self):
        lexer = Lexer(StubIo("someId1213"))
        token = lexer.get_token()
        self.assertTrue(isinstance(token, Token))
        self.assertEqual(token.kind, TokenType.ID)

        self.assertTrue(isinstance(token.val, SymbolEntry))
        self.assertEqual(token.val.kind, TokenType.ID)
        self.assertEqual(token.val.val, "someId1213")
        self.assertEqual(token.val.line, 1)

    def test_ws(self):
        lexer = Lexer(StubIo("  \t \n "))
        token = lexer.get_token()
        self.assertIsNone(token)

        lexer = Lexer(StubIo("\n"))
        token = lexer.get_token()
        self.assertIsNone(token)

if __name__ == "__main__":
    unittest.main()

