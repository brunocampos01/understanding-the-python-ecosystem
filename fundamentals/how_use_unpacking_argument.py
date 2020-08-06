"""
https://docs.python.org/3/tutorial/controlflow.html
"""


def parrot(voltage, state='a stiff', action='voom'):
    print("-- This parrot wouldn't", action, end=' ')
    print("if you put", voltage, "volts through it.", end=' ')
    print("E's", state, "!")


d = {"voltage": "four million",
     "state": "bleedin' demised",
     "action": "VOOM"}

if __name__ == '__main__':
    parrot(**d)
