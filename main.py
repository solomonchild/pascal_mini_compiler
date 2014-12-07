from pascal_parser.lexer import *
from pascal_parser.parser import *
import sys

def main():
    fileName = None
    if len(sys.argv) > 1:
        fileName = sys.argv[1]
    stream = FileStream(fileName)
    lexer = Lexer(stream)
    parser = Parser(lexer)
    result = parser.parse()
    if not result:
        print("\nInvalid syntax")
        return
    else:
        print("\nSuccessfully recognized syntax")
    
    print("\nPrinting a table of lexemes:\n")
    lexer.printTable(lexer.lexemes)

    print("\nPrinting a table of keywords:\n")
    lexer.printTable(lexer.keywords)
    print("\nPrinting a table of literals:\n")
    lexer.printTable(lexer.literals)
    print("\nPrinting a table of IDs:\n")
    lexer.printTable(lexer.identifiers)
    

if __name__ == "__main__":
    main()
