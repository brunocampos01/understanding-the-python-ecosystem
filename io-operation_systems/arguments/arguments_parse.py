"""
python [file].py [command] [options] NAME
python argparse/commands.py --help

https://docs.python.org/3/howto/argparse.html
"""
import argparse


parser = argparse.ArgumentParser()
subparsers = parser.add_subparsers()
parser.add_argument('--version', action='version', version='1.0.0')


hello_parser = subparsers.add_parser('hello')
goodbye_parser = subparsers.add_parser('gogfdfgodbye')

if __name__ == '__main__':
    args = parser.parse_args()
