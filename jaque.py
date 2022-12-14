from tokens import StringToken, IntToken, FloatToken, WordToken, CharToken, EOFToken, Token
from exceptions import UnexpectedToken, UnrecognizedToken


class Tokenizer:
    def __init__(self, content):
        self.index = 0             # current character index
        self.line = 0              # keeping track of the line
        self.col = 0               # and the column
        self.content = content     # string content

    def advance(self):
        self.col += 1
        self.index += 1

    def eof(self):
        return self.index >= len(self.content)

    def get_char(self):
        if self.eof():
            raise UnexpectedToken(EOFToken(), Token(), self.content)

        return self.content[self.index]

    def read_word(self):
        word = ""

        # these are the characters for "true", "false", "null"
        # no other keywords can exist
        while self.get_char() in "truefalsn":
            word += self.content[self.index]
            self.advance()

        self.index -= 1
        self.col -= 1

        return word

    def tokenize_string(self):
        if (self.index + 1 >= len(self.content)):
            raise UnexpectedToken(EOFToken(line=self.line, col=self.col), CharToken('"'), self.content)

        final = self.content.find('"', self.index + 1)
        if final == -1:
            raise UnexpectedToken(EOFToken(line=self.line, col=self.col), CharToken('"'), self.content)

        # get the string betweeen the ""
        tok = StringToken(self.content[self.index + 1:final], self.line, self.col)
        self.col += final - self.index
        self.index = final

        return tok

    def tokenize_number(self):
        is_int = True
        number = ""

        current_char = self.get_char()

        # we allow - because numbers can be negative
        if current_char == '-':
            number += current_char
            self.advance()

        while not self.eof():
            current_char = self.get_char()

            # if we find a . that means that the number
            # is floating point
            if current_char == '.':
                if not is_int:
                    # can't be two or more . in a float number
                    raise UnexpectedToken(CharToken('.', line=self.line, col=self.col), IntToken(), self.content)

                number += current_char
                is_int = False

            elif current_char.isdigit():
                number += current_char

            else:
                # decrease index because the get_next_token will increase it
                # anyway so we don't skip characters
                self.index -= 1
                self.col -= 1
                return is_int and IntToken(int(number), self.line, self.col) or FloatToken(float(number), self.line, self.col)

            self.advance()

    def get_next_token(self):
        # if we are at the end of the string we
        # return an EOF token, this makes it easy
        # for the parser to know when the string ends
        if self.eof():
            return EOFToken(line=self.line, col=self.col)

        current_char = self.get_char()

        # ignoring whitespaces
        while current_char in " \r\f\t\n":
            if current_char == '\n':
                self.line += 1
                self.col = -1

            self.advance()
            if self.eof():
                return EOFToken(line=self.line, col=self.col)

            current_char = self.get_char()

        if current_char == '"':
            tok = self.tokenize_string()

        elif current_char == '-' or current_char.isdigit():
            tok = self.tokenize_number()

        elif current_char in '{}[]:,':
            tok = CharToken(current_char, self.line, self.col)
        else:
            word = self.read_word()
            if word in ["true", "false", "null"]:
                tok = WordToken(word, self.line, self.col - len(word))
            else:
                raise UnrecognizedToken(word, self.line, self.col - len(word), self.content)

        self.advance()
        return tok


class Parser:
    def __init__(self, content):
        self.content = content
        self.tokenizer = Tokenizer(content)
        self.current_token = None

    def get_tok(self):
        return self.current_token

    def advance(self):
        # get the next token from the tokenizer
        self.current_token = self.tokenizer.get_next_token()

    def get_advance(self):
        tok = self.get_tok()
        self.advance()
        return tok

    def check_char(self, char):
        token = self.get_tok()
        return token == CharToken(char)

    def expect_string(self, token):
        if type(token) is not StringToken:
            raise UnexpectedToken(token, StringToken(), self.content)

    def expect_char(self, char):
        # if we do not have what we are expecting
        # then the json is not valid so we throw an
        # UnexpectedToken exception
        token = self.get_advance()
        if token != CharToken(char):
            raise UnexpectedToken(token, CharToken(char), self.content)

    def parse_value(self):
        current_token = self.get_tok()

        if current_token == CharToken('{'):
            return self.parse_object()

        if current_token == CharToken('['):
            return self.parse_list()

        self.advance()

        if current_token == WordToken('true'):
            return True

        if current_token == WordToken('false'):
            return False

        if current_token == WordToken('null'):
            return None

        elif type(current_token) in (IntToken, FloatToken, StringToken):
            return current_token.value

        raise Exception(f"unexpected token: {current_token}")

    def parse_object(self):
        self.expect_char("{")

        obj = {}

        while True:
            # the dict can be empty or containing a , before
            # it ends
            if self.check_char('}'):
                break

            key = self.get_advance()
            self.expect_string(key)

            self.expect_char(":")

            value = self.parse_value()

            obj[key.value] = value

            # if we have nor more , we stop
            if not self.check_char(","):
                break

            self.advance()

        self.expect_char("}")

        return obj

    def parse_list(self):
        self.expect_char("[")

        values = []
        while True:
            # the list can be empty or containing a , before
            # it ends
            if self.check_char("]"):
                break

            value = self.parse_value()
            values.append(value)

            # if we have nor more , we stop
            if not self.check_char(","):
                break

            self.advance()

        self.expect_char("]")

        return values

    def parse_body(self):
        self.advance()

        # only dict or list can be root
        if self.check_char('{'):
            return self.parse_object()

        if self.check_char('['):
            return self.parse_list()

    def parse(self, content):
        return self.parse_body()


def LoadString(content):
    parser = Parser(content)
    return parser.parse(content)


if __name__ == "__main__":
    import json
    import sys

    test_string = len(sys.argv) > 1 and sys.argv[1] or '{"a": 10, "b": [10, {"z": 100}]}'
    print(json.dumps(LoadString(test_string)))
