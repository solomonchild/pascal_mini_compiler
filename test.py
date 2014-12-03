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


    def setUp(self):
        def awaitKind(self, test, awaitedKind, awaitedVal):
            test.assertTrue(isinstance(self, Token))
            test.assertEqual(self.kind, awaitedKind)
            test.assertEqual(self.val, awaitedVal)

        def awaitId(self, test, val, line):
            test.assertTrue(isinstance(self, Token))
            test.assertEqual(self.kind, TokenType.ID)

            test.assertTrue(isinstance(self.val, SymbolEntry))
            test.assertEqual(self.val.kind, TokenType.ID)
            test.assertEqual(self.val.val, val)
            test.assertEqual(self.val.line, line)
        Token.awaitId = awaitId
        Token.awaitKind = awaitKind

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
        token.awaitId(self, "someId1213", 1)

    def test_ws(self):
        lexer = Lexer(StubIo("  \t \n "))
        token = lexer.get_token()
        self.assertIsNone(token)

        lexer = Lexer(StubIo("\n"))
        token = lexer.get_token()
        self.assertIsNone(token)

    def test_less_signs(self):
        lexer = Lexer(StubIo("< <="))

        token = lexer.get_token()
        token.awaitKind(self, TokenType.OPERATOR, "<")

        token = lexer.get_token()
        token.awaitKind(self, TokenType.OPERATOR, "<=")


    def test_greater_signs(self):
        lexer = Lexer(StubIo("> >="))

        token = lexer.get_token()
        token.awaitKind(self, TokenType.OPERATOR, ">")

        token = lexer.get_token()
        token.awaitKind(self, TokenType.OPERATOR, ">=")

    def test_equ_operators(self):
        lexer = Lexer(StubIo("== <>"))

        token = lexer.get_token()
        token.awaitKind(self, TokenType.OPERATOR, "==")

        token = lexer.get_token()
        token.awaitKind(self, TokenType.OPERATOR, "<>")

    def test_integers(self):
        lexer = Lexer(StubIo("10 01 23 -23"))

        token = lexer.get_token()
        token.awaitKind(self, TokenType.INTEGER, "10")

        token = lexer.get_token()
        token.awaitKind(self, TokenType.INTEGER, "01")

        token = lexer.get_token()
        token.awaitKind(self, TokenType.INTEGER, "23")

        token = lexer.get_token()
        token.awaitKind(self, TokenType.INTEGER, "-23")


    def test_function_call(self):
        lexer = Lexer(StubIo("UpperCase(someArg);"))

        token = lexer.get_token()
        token.awaitId(self, "UpperCase", 1)

        token = lexer.get_token()
        token.awaitKind(self, TokenType.LPAREN, "(")

        token = lexer.get_token()
        token.awaitId(self, "someArg", 1)

        token = lexer.get_token()
        token.awaitKind(self, TokenType.RPAREN, ")")

        token = lexer.get_token()
        token.awaitKind(self, TokenType.SEMICOLON, ";")


    def test_assignment(self):
        lexer = Lexer(StubIo("Key := UpCase;"))

        token = lexer.get_token()
        token.awaitId(self, "Key", 1)

        token = lexer.get_token()
        token.awaitKind(self, TokenType.ASSIGN, ":=")

        token = lexer.get_token()
        token.awaitId(self, "UpCase", 1)

        token = lexer.get_token()
        token.awaitKind(self, TokenType.SEMICOLON, ";")



if __name__ == "__main__":
    unittest.main()

