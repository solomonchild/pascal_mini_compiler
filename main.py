from lexer import *

def main():
    lexer = Lexer("input.pas")

    while True:
        line =  lexer.get_token()
        if line == None:
            break
        print line
    lexer.print_stable()
    

if __name__ == "__main__":
    main()
