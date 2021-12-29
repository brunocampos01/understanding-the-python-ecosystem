class Animal:
    __hungry = "yes"
    __name = "no name"
    __owner = "no owner"

    def __init__(self):
        pass

    def set_owner(self, new_owner):
        self.__owner = new_owner
        return

    def get_owner(self):
        return self.__owner

    def set_name(self, new_name):
        self.__name = new_name
        return

    def get_name(self):
        return self.__name

    def noise(self):
        print('errr')
        return

    @staticmethod
    def __hidden_method():
        print("hard to find")


def main():
    # Indentation is OUT class
    dog = Animal()
    dog.set_owner('Sue')
    print(dog.get_owner())
    dog.noise()


if __name__ == '__main__':
    main()
