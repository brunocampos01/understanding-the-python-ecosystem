class Stack(object):

    def __init__(self):
        """Constructor"""
        self.stack = []
        self.count = 0

    def push(self, element):
        """Insert on top stack"""
        self.stack.append(element)
        self.count += 1

    def pop(self):
        """Remove on top stack"""
        if not self.is_empty():
            self.stack.pop(self.count - 1)
            self.count -= 1

    def remove_all_elements(self):
        """Remove all"""
        self.stack = []
        self.count = 0

    def get_top(self):
        """Get the last"""
        if not self.is_empty():
            return self.stack[-1]

        return None

    def is_empty(self) -> bool:
        """Check if the stack is empty"""
        if self.count == 0:
            return True

        return False

    def get_length(self) -> int:
        """Return the size"""
        return self.count

    def show_stack(self):
        """Show each element on stack"""
        if self.is_empty():
            print('Stack is empty')
        else:
            for e in reversed(self.stack):
                print(e)
