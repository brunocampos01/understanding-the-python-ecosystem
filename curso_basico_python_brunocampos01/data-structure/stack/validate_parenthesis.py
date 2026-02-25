"""
Given a string containing just the characters '(', ')', '{', '}', '[' and ']',
determine if the input string is valid.

The brackets must close in the correct order,
"()" and "()[]{}" are all valid.
"""


def is_valid(s: str) -> bool:
    stack = []
    mapping = {
        ")": "(",
        "}": "{",
        "]": "["
    }

    for char in s:
        if char in mapping.values():
            stack.append(char)
            print(f'stack = {stack}')
        elif char in mapping:
            if not stack or mapping[char] != stack[-1]:
                print("Unbalanced\n")
                return False
            stack.pop()

    if not stack:
        print("Balanced\n")
        return True
    else:
        print("Unbalanced\n")
        return False


def main():
    assert is_valid('()') is True
    assert is_valid('[]') is True
    assert is_valid('{}') is True
    assert is_valid('{[]{()}}') is True

    assert is_valid('[{}{})(]') is False
    assert is_valid('((()') is False
    assert is_valid('][') is False
    assert is_valid(')') is False


if __name__ == '__main__':
    main()
