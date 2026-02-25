import argparse
import sys


def fibonacci(input_number):
    previous, nxt = 0, 1
    for number in range(input_number):
        previous, nxt = nxt, previous + nxt

    return previous


def execute(parser):
    """
    Execute the Fibonacci sequence with the given argument,
    along with several optional arguments and -h for help.
    """

    parser.add_argument(
        "number",
        help="The position in the Fibonacci sequence to compute",
        type=int
    )

    parser.add_argument(
        "-o",
        "--output",
        help="Write the output to a separate file",
        action="store"
    )

    group = parser.add_mutually_exclusive_group()

    group.add_argument(
        "-v",
        "--verbose",
        help="Print the output in verbose mode",
        action="store_true"
    )
    group.add_argument(
        "-q",
        "--quiet",
        help="Print the output in quiet mode",
        action="store_true"
    )

    args = parser.parse_args()

    result = fibonacci(args.number)

    if args.output is not None:
        with open(args.output, 'a') as file:
            original_stdout = sys.stdout
            try:
                sys.stdout = file
                _print_result(args, result)
            finally:
                sys.stdout = original_stdout
    else:
        _print_result(args, result)


def _print_result(args, result):
    if args.verbose:
        print("The", args.number, "value of the Fibonacci sequence is", result)
    elif args.quiet:
        print(result)
    else:
        print("Fibonacci(" + str(args.number) + ") =", result)


def main():
    parser = argparse.ArgumentParser(description="Argparse example")
    execute(parser)


if __name__ == '__main__':
    main()
