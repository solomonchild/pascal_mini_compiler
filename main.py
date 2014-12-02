from lexer import *

def main():
    stream = FileStream("input.pas")
    lexer = Lexer(stream)

    while True:
        line =  lexer.get_token()
        if line == None:
            break
        print(line)
    

if __name__ == "__main__":
    main()
