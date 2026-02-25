class Animal:
    def __init__(self, name="no name", owner="no owner", hungry=True):
        self._name = name
        self._owner = owner
        self._hungry = hungry

    @property
    def owner(self):
        return self._owner

    @owner.setter
    def owner(self, new_owner):
        self._owner = new_owner

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, new_name):
        self._name = new_name

    def noise(self):
        print('errr')

    @staticmethod
    def _hidden_method():
        print("hard to find")


def main():
    dog = Animal()
    dog.owner = 'Sue'
    print(dog.owner)
    dog.noise()


if __name__ == '__main__':
    main()
