def _get_line_index(content, line):
    index = 0

    while line > 0:
        index = content.find("\n", index)
        if index == -1:
            raise Exception("something wrong")

        index += 1
        line -= 1

    return index


class JsonException(Exception):
    def __init__(self, message, content, line, col):
        self.message = message + '\n\n'
        index = _get_line_index(content, line) + col
        lower = max(index - 20, 0)
        higher = min(index + 21, len(content))

        trunked_text = content[lower:higher]

        self.message += trunked_text + "\n"
        self.message += " " * (index - lower) + "^" + " " * (max(higher - 1, 0) - index) + "\n"

    def __str__(self):
        return self.message

    def __repr__(self):
        return str(self)


class UnexpectedToken(JsonException):
    def __init__(self, token, expected, content):
        super().__init__(f"unexpected token: {str(token)}, expected: {expected}", content, token.line, token.col)


class UnrecognizedToken(JsonException):
    def __init__(self, token, content, line, col):
        super().__init__(f"Unrecognized token: {token}", content, line, col)
