"""Greeter.

Usage:
  basic.py hello <name> [--caps] [--greeting=<str>]
  basic.py goodbye <name> [--caps] [--greeting=<str>]
  basic.py (-h | --help)

Options:
  -h --help         Show this screen.
  --caps            Uppercase the output.
  --greeting=<str>  Greeting to use [default: Hello].

Commands:
   hello       Say hello
   goodbye     Say goodbye

"""
from docopt import docopt

HELLO = """usage: basic.py hello [options] [<name>]

  -h --help         Show this screen.
  --caps            Uppercase the output.
  --greeting=<str>  Greeting to use [default: Hello].
"""

GOODBYE = """usage: basic.py goodbye [options] [<name>]

  -h --help         Show this screen.
  --caps            Uppercase the output.
  --greeting=<str>  Greeting to use [default: Goodbye].
"""


def greet(args):
    output = '{0}, {1}!'.format(args['--greeting'],
                                args['<name>'])
    if args['--caps']:
        output = output.upper()
    print(output)


if __name__ == '__main__':
    arguments = docopt(__doc__, options_first=True)

    if arguments['<command>'] == 'hello':
        greet(docopt(HELLO))
    elif arguments['<command>'] == 'goodbye':
        greet(docopt(GOODBYE))
    else:
        exit("{0} is not a command. \
          See 'options.py --help'.".format(arguments['<command>']))
