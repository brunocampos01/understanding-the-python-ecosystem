"""
For example:
bottom [6, 3, 5, 1, 2, 4] top
The function should return false

bottom [1, 2, 3, 4, 5, 6] top
The function should return true
"""


def is_sorted(stack: list) -> bool:
    """Check if a stack is sorted from bottom (smallest) to top (largest)."""
    storage_stack = []
    sorted_flag = True

    while len(stack) > 1:
        top = stack.pop()
        storage_stack.append(top)

        if stack[-1] > top:
            sorted_flag = False
            break

    while storage_stack:
        stack.append(storage_stack.pop())

    if sorted_flag:
        print('The stack is sorted')
    else:
        print('The stack is unsorted')

    return sorted_flag


def main():
    is_true = [1, 2, 3, 4, 5, 6]
    is_false = [6, 3, 5, 1, 2, 4]

    assert is_sorted(stack=is_true) is True
    assert is_sorted(stack=is_false) is False


if __name__ == '__main__':
    main()
