"""
For example:
bottom [6, 3, 5, 1, 2, 4] top
The function should return false

bottom [1, 2, 3, 4, 5, 6] top
The function should return true
"""


def is_sorted(stack: list):
    storage_stack = []

    for i in range(len(stack)):

        first_value = stack.pop()
        if len(stack) == 0:  # Case odd number of values in stack
            print('The stack is sorted')
            return True

        second_value = stack.pop()
        if first_value - second_value != 1:  # Not consecutive
            print('The stack is unsorted')
            return False

        stack.append(second_value)  # Backup second value
        storage_stack.append(first_value)

    # Back up stack from storage stack
    for i in range(len(storage_stack)):
        stack.append(storage_stack.pop())

    return True


def main():
    is_true = [1, 2, 3, 4, 5, 6]
    is_false = [6, 3, 5, 1, 2, 4]

    is_sorted(stack=is_true)
    is_sorted(stack=is_false)


if __name__ == '__main__':
    main()
