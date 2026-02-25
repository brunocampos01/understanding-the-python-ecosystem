class Stack:

    def __init__(self):
        self.stack = []
        self.count = 0

    def push(self, element):
        """Insert on top of stack."""
        self.stack.append(element)
        self.count += 1

    def pop(self):
        """Remove and return the top element of the stack."""
        if not self.is_empty():
            self.count -= 1
            return self.stack.pop(self.count)
        return None

    def remove_all_elements(self):
        """Remove all elements."""
        self.stack = []
        self.count = 0

    def get_top(self):
        """Get the top element without removing it."""
        if not self.is_empty():
            return self.stack[-1]
        return None

    def is_empty(self) -> bool:
        """Check if the stack is empty."""
        return self.count == 0

    def get_length(self) -> int:
        """Return the size."""
        return self.count

    def show_stack(self):
        """Show each element on stack."""
        if self.is_empty():
            print('Stack is empty')
        else:
            for e in reversed(self.stack):
                print(e)
