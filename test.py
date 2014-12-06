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

    def putChar(self, howMany = 1):
        self.pos -= 1

    def getChar(self):
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
            entry = self.table[self.idx]
            test.assertIsNotNone(entry)
            test.assertEqual(entry.val, awaitedVal)
            test.assertEqual(entry.kind, awaitedKind)

        def awaitUnknown(self, test, awaitedVal):
            test.assertTrue(isinstance(self, Token))
            test.assertEqual(self.val, awaitedVal)

        Token.awaitKind = awaitKind
        Token.awaitUnknown = awaitUnknown

    def teardown(self):
        pass
    
    def test_keyword(self):
        lexer = Lexer(StubIo("var"))
        token = lexer.getToken()
        self.assertTrue(isinstance(token, Token))
        self.assertEqual(token.kind, TokenType.VAR)
        self.assertEqual(token.val, "var")

    def test_keyword(self):
        lexer = Lexer(StubIo("var"))
        token = lexer.getToken()
        self.assertTrue(isinstance(token, Token))
        self.assertEqual(token.kind, TokenType.VAR)
        self.assertEqual(token.val, "var")

    def test_id_starts_with_num(self):
        lexer = Lexer(StubIo("1procedure"))

        token = lexer.getToken()

        self.assertTrue(isinstance(token, Token))
        token.awaitUnknown(self, "1procedure")

    def test_id(self):
        lexer = Lexer(StubIo("someId1213"))

        token = lexer.getToken()

        self.assertTrue(isinstance(token, Token))
        token.awaitKind(self, TokenType.ID, "someId1213")

    def test_ws(self):
        lexer = Lexer(StubIo("  \t \n "))
        token = lexer.getToken()
        self.assertIsNone(token)

        lexer = Lexer(StubIo("\n"))
        token = lexer.getToken()
        self.assertIsNone(token)

    def test_less_signs(self):
        lexer = Lexer(StubIo("< <="))

        token = lexer.getToken()
        token.awaitKind(self, TokenType.OPERATOR, "<")

        token = lexer.getToken()
        token.awaitKind(self, TokenType.OPERATOR, "<=")


    def test_greater_signs(self):
        lexer = Lexer(StubIo("> >="))

        token = lexer.getToken()
        token.awaitKind(self, TokenType.OPERATOR, ">")

        token = lexer.getToken()
        token.awaitKind(self, TokenType.OPERATOR, ">=")

    def test_equ_operators(self):
        lexer = Lexer(StubIo("= <>"))

        token = lexer.getToken()
        token.awaitKind(self, TokenType.OPERATOR, "=")

        token = lexer.getToken()
        token.awaitKind(self, TokenType.OPERATOR, "<>")

    def test_literal(self):
        lexer = Lexer(StubIo("'Hi there1234@#!I\\'m a string\"\"'"))
        token = lexer.getToken()
        token.awaitKind(self, TokenType.STRING, "Hi there1234@#!I\'m a string\"\"")

        lexer = Lexer(StubIo('\"Hi there1234@#!I\'m a string\\"\"'))
        token = lexer.getToken()
        token.awaitKind(self, TokenType.STRING, "Hi there1234@#!I\'m a string\"")

        lexer = Lexer(StubIo('"Some str", "some str"'))
        token = lexer.getToken()
        token.awaitKind(self, TokenType.STRING, "Some str")

        token = lexer.getToken()
        token.awaitKind(self, TokenType.COMMA, ",")

        token = lexer.getToken()
        token.awaitKind(self, TokenType.STRING, "some str")

    def test_integers(self):
        lexer = Lexer(StubIo("10 01 23 -23"))

        token = lexer.getToken()
        token.awaitKind(self, TokenType.INTEGER, "10")

        token = lexer.getToken()
        token.awaitKind(self, TokenType.INTEGER, "01")

        token = lexer.getToken()
        token.awaitKind(self, TokenType.INTEGER, "23")

        token = lexer.getToken()
        token.awaitKind(self, TokenType.INTEGER, "-23")


    def test_function_call(self):
        lexer = Lexer(StubIo("UpperCase(someArg);"))

        token = lexer.getToken()
        token.awaitKind(self, TokenType.ID, "UpperCase")

        token = lexer.getToken()
        token.awaitKind(self, TokenType.LPAREN, "(")

        token = lexer.getToken()
        token.awaitKind(self, TokenType.ID,  "someArg")

        token = lexer.getToken()
        token.awaitKind(self, TokenType.RPAREN, ")")

        token = lexer.getToken()
        token.awaitKind(self, TokenType.SEMICOLON, ";")


    def test_parens(self):
        lexer = Lexer(StubIo("[]"))

        token = lexer.getToken()
        token.awaitKind(self, TokenType.LSQUARE, "[")

        token = lexer.getToken()
        token.awaitKind(self, TokenType.RSQUARE, "]")

    def test_real(self):
        lexer = Lexer(StubIo("+0.9 -25.5 19.9"))

        token = lexer.getToken()
        token.awaitKind(self, TokenType.REAL, "+0.9")

        token = lexer.getToken()
        token.awaitKind(self, TokenType.REAL, "-25.5")

        token = lexer.getToken()
        token.awaitKind(self, TokenType.REAL, "19.9")

    def test_integer(self):
        lexer = Lexer(StubIo("+09 -25 -500"))

        token = lexer.getToken()
        token.awaitKind(self, TokenType.INTEGER, "+09")

        token = lexer.getToken()
        token.awaitKind(self, TokenType.INTEGER, "-25")

        token = lexer.getToken()
        token.awaitKind(self, TokenType.INTEGER, "-500")

    def test_assignment(self):
        lexer = Lexer(StubIo("Key := UpCase;"))

        token = lexer.getToken()
        token.awaitKind(self, TokenType.ID,  "Key")

        token = lexer.getToken()
        token.awaitKind(self, TokenType.ASSIGN, ":=")

        token = lexer.getToken()
        token.awaitKind(self, TokenType.ID,  "UpCase")

        token = lexer.getToken()
        token.awaitKind(self, TokenType.SEMICOLON, ";")



if __name__ == "__main__":
    unittest.main()

