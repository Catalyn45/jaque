# Jaque

Jaque is a simple json parser written in python. The purpose of this project
is to learn how to make a parser.

# Usage

you can use the `LoadString` function to parse a `json` text
into a python `dict`

examples for testing:

`python jaque.py '{"a": 10, "b": "dog"}'`
`cat ./json_file.json | xargs python jaque.py`

you can run the tests with
`python tests.py`

# Grammar

```
BODY:      OBJECT |
           LIST

OBJECT:    "{" ( OBJECT_EL ("," OBJECT_EL)* ","?)? "}"

OBJECT_EL: STRING ":" VALUE

LIST:      "{" ( VALUE ("," VALUE)* ","?)? "}"

VALUE:     OBJECT |
           LIST   |
           STRING |
           INT    |
           FLOAT  |
           "true" |
           "false"|
           "null"
```
