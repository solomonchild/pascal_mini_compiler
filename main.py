from lexer import *

def main():
    stream = FileStream("input.pas")
    lexer = Lexer(stream)

    while True:
        line =  lexer.get_token()
        if line == None:
            break
        elif line.kind == TokenType.UNKNOWN:
            print("\nError: Unknown lexeme {0} at line {1}".format(line.val, lexer.stream.current_line_num()))
            return
        print(line)

    print("\nSuccess: got a stream of tokens")
    
    print("\nPrinting a table of keywords:\n")
    lexer.printTable(lexer.keywords)
    print("\nPrinting a table of literals:\n")
    lexer.printTable(lexer.literals)
    print("\nPrinting a table of IDs:\n")
    lexer.printTable(lexer.identifiers)
    

if __name__ == "__main__":
    main()
