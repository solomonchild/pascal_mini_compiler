from .lexer import *

#<G> ::= <S>
#<S> ::= if <E> then <S> | <ID> := <STRING> ;
#<E> ::= <ID> <OP> <ID> | <ID> <OP> <STRING> | (<E>) and (<E>)
#<ID> ::= [a-zA-Z_][a-zA-Z0-9_]*
#<OP> ::= - | + | * | / 

class Parser:

    def __init__(self, lexer): 
        self.lexer = lexer
        self.tokens = None
        self.token = None
        self.token_n = 0
        self.saved = 0

    def term(self, t):
        if not self.nextToken():
            return False
        #print("Current token {0} {1}, term: {2}".format(self.token.kind, self.token.val, t))
        if self.token.kind == t:
            #print("Match")
            return True
        else:
            #print("Not matched")
            self.pushTokens()
            return False



    def restoreToken(self):
        self.token_n = self.saved
        self.token = self.tokens[self.token_n]
        return True

    def saveToken(self):
        self.saved = self.token_n

    def pushTokens(self, num = 1):
        if num < 0 or num > self.token_n:
            raise Exception("Invalid number of tokens")
        while num:
            num -= 1
            self.token_n -= 1
            self.token = self.tokens[self.token_n]

    def nextToken(self):
        if self.token_n > len(self.tokens) - 1:
            return False
        self.token = self.tokens[self.token_n]
        self.token_n += 1
        return True

    def E(self):
        self.saveToken()
        return (self.term(TokenType.ID) and  self.term(TokenType.OPERATOR) and self.term(TokenType.ID)) or \
                   (self.restoreToken() and self.term(TokenType.ID) and  self.term(TokenType.OPERATOR) and self.term(TokenType.STRING)) or \
                   (self.restoreToken() and self.term(TokenType.LPAREN) and self.E() and self.term(TokenType.RPAREN) and self.term(TokenType.AND) and self.term(TokenType.LPAREN) and self.E() and self.term(TokenType.RPAREN))

    def S(self):
        self.saveToken()
        return (self.term(TokenType.IF) and self.E() and self.term(TokenType.THEN) and self.S()) or \
            (self.restoreToken() and self.term(TokenType.ID) and self.term(TokenType.ASSIGN) and self.term(TokenType.STRING) and self.term(TokenType.SEMICOLON))

    def parse(self):
        while True:
            token = self.lexer.getToken()
            if token == None:
                break
            elif token.kind == TokenType.UNKNOWN:
                print("\nError: Unknown lexeme {0} at line {1}".format(token.val, self.lexer.stream.currentLineNum()))
                return
        self.tokens = self.lexer.lexemes
        result = self.S() and self.token_n == len(self.tokens)
        if not result:
            print("Invalid token \"{0}\" of type {1} at line {2}".format(self.token.val, self.token.kind, self.token.line))
        return result

