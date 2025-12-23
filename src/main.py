import sys
import parser as parse
from lexer import get_tokens


def main():
  with open(sys.argv[1], "r") as file:
    content = file.read()
  tokens = get_tokens(content[0])
  parse.main(tokens)

main()



