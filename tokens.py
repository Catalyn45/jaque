class Token:
    def __init__(self, value=None, line=-1, col=-1):
        self.value = value
        self.line = line
        self.col = col

    def __str__(self):
        return f"{{ {type(self).__name__} => '{self.value}' }}"

    def __repr__(self):
        return str(self)

    def __eq__(self, other):
        if isinstance(other, Token):
            return type(self) is type(other) and self.value == other.value


class StringToken(Token):
    pass


class IntToken(Token):
    pass


class FloatToken(Token):
    pass


class WordToken(Token):
    pass


class CharToken(Token):
    pass


class EOFToken(Token):
    pass
