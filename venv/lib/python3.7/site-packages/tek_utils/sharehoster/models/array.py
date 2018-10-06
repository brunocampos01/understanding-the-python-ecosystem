class Array(object):

    def __init__(self, *values):
        self.values = list(values)

    def __add__(self, other):
        new_values = [left + right for left, right in zip(self.values,
                                                          other.values)]
        return Array(new_values)

    def __sub__(self, other):
        new_values = [left - right for left, right in zip(self.values,
                                                          other.values)]
        return Array(*new_values)

    def __getitem__(self, index):
        return self.values[index]

__all__ = []
