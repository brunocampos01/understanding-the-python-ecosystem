"""
Reference: https://docs.python.org/3/tutorial/controlflow.html
"""


def parrot(voltage, state='a stiff', action='voom', type='Norwegian Blue'):
    """
    Accepts one required argument (voltage)
    and three optional arguments (state, action, and type).

    Params
    :param voltage: required
    :param state: optional
    :param action: optional
    :param type: optional
    """
    print("-- This parrot wouldn't", action, end=' ')
    print("if you put", voltage, "volts through it.")
    print("-- Lovely plumage, the", type)
    print("-- It's", state, "!")


if __name__ == '__main__':
    parrot(1000)  # 1 positional argument
    parrot(voltage=1000)  # 1 keyword argument
    parrot(voltage=1000000, action='VOOOOOM')  # 2 keyword arguments
    parrot(action='VOOOOOM', voltage=1000000)  # 2 keyword arguments
    parrot('a million', 'bereft of life', 'jump')  # 3 positional arguments
    parrot('a thousand', state='pushing up the daisies')  # 1 positional, 1 keyword

    # Invalid
    # parrot()                     # required argument missing
    # parrot(voltage=5.0, 'dead')  # non-keyword argument after a keyword argument
    # parrot(110, voltage=220)     # duplicate value for the same argument
    # parrot(actor='John Cleese')  # unknown keyword argument
