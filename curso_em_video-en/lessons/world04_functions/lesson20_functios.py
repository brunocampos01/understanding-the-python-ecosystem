"""
Defining Functions
Default Arguments
Variable Scope
Documentation
function recursive
Lambda Expressions
"""

# Defining Functions
if False:
    def show_plus_ten(num):
        return num + 10


    print(show_plus_ten(500))

# Default Arguments
if False:
    def cylinder_volume(height, radius=5):  # radius is parameter optional
        pi = 3.14
        return height * pi * radius ** 2


    print(cylinder_volume(2))  # unspecified in a function call.
    print(cylinder_volume(10, 7))  # pass in arguments by position
    print(cylinder_volume(height=10, radius=7))  # pass in arguments by name

# Variable scope and global scope
if False:
    # This will result in an error
    def some_function():
        word = "hello"


    print(some_function())

if True:
    # This works fine
    word = "hello"


    def some_functionGlobal():
        print(word)


    some_functionGlobal()

'''Good practice:
It is best to define variables in the smallest scope they will be needed in.
While functions can refer to variables defined in a larger scope, this is very rarely a good idea.'''

if False:
    def population_density(population, land_area):
        """Calculate the population density of an area.

        INPUT:
        population: int. The population of that area
        land_area: int or float. This function is unit-agnostic, if you pass in values in terms
        of square km or square miles the function will return a density in those units.

        OUTPUT:
        population_density: population / land_area. The population density of a particular area.

        ERRORS:
        when a key error
        """
        return population / land_area

# function recursive
if False:
    def fatorial(n):
        if n == 0 or n == 1:
            return 1
        else:
            return n * fatorial(n - 1)


    print('fatorial de {} : {}'.format(5, fatorial(5)))


    def fibonacci(n):
        if n <= 1:
            return n
        else:
            return fibonacci(n - 1) + fibonacci(n - 2)


    print('Fibonacci: {}'.format(fibonacci(20)))

# function lambda
'''
1. The lambda keyword is used to indicate that this is a lambda expression. 
2. Following lambda are one or more arguments for the anonymous function separated by commas,followed by a colon :
3. Last is an expression that is evaluated and returned in this function. 
'''
if False:
    def multiply(x, y):
        return x * y


    # equals
    multiplys = lambda x, y: x * y

    print(multiplys(2, 6))
