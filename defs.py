class TokenType:
    LPAREN = 0
    RPAREN = 1
    names = [
        "LPAREN",
        "RPAREN"
    ]

    @staticmethod
    def map_kind_to_str(kind):
        return TokenType.names[kind]

