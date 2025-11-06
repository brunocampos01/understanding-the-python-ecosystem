"""
Given a string containing just the characters '(', ')', '{', '}', '[' and ']',
determine if the input string is valid.

The brackets must close in the correct order,
"()" and "()[]{}" are all valid.
"""


def is_valid(s: str) -> bool:
    # The stack to keep track of opening brackets.
    stack = []
    mapping = {
        ")": "(",
        "}": "{",
        "]": "["
    }

    for char in s:
        if char in mapping.values():  # open
            stack.append(char)
            print(f'stack = {stack}')

        elif char in mapping.keys():
            if len(stack) > 0 and mapping[char] == stack[len(stack) - 1]:
                stack.pop()

    # if the stack is empty, then we have a valid expression.
    if len(stack) == 0:
        print("Balanced\n")
        return True
    else:
        print("Unbalanced\n")
        return False


def main():
    is_valid('()')
    is_valid('[]')
    is_valid('{}')

    is_valid('{[]{()}}')
    is_valid('[{}{})(]')
    is_valid('((()')


if __name__ == '__main__':
    main()
