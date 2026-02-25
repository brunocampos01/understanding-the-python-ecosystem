class MyFirstClass:
    """A simple example class"""
    i = 42

    def func_ex(self):
        print('learning Python')


if __name__ == '__main__':
    instance = MyFirstClass()
    instance.func_ex()

    print(instance.__class__)
