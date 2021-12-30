# Becoming a Expert Python
![License](https://img.shields.io/badge/Code%20License-MIT-blue.svg)
![Python 3](https://img.shields.io/badge/python-3-yellow.svg)

<img src='images/python.png' align="center" height=auto width=80%>


These guides aim to understand the development and execution environment of Python. In addition, I will cover topics ranging from language fundamentals, good practices, build, deploy, distribution to advanced language programming topics.

_Estes guias tem por objetivo compreender o ambiente de desenvolvimento e execução de Python. Além disso, vou cobrir tópicos que envolvem desde os fundamentos da linguagem, boas práticas, build, deploy e distribuição_

- NOTE: Tópicos avançados de programação com Python ficaram em outro contexto.

# Summary
[ How to install and set up a Python](#how-to-install-and-set-up-a-Python)

## Preparing the Environment for the Python
This topic describe how to set up the environment to Python developement.
- [Check Python Configuration](#check-python-configuration)
- [Preparing Environment](#preparing-environment)
- [Requirements File](#requirements-file)
- [Virtual Environment](#virtual-environment)
- [Pipenv](#pipenv)

## Fundamentals
- [What's is Python ?](#what's-is-python-?)
- [Zen of Python](#zen-of-python)
- [Types](#types)
- [Interpreter and Compiler](#interpreter-and-compiler)
- [Complete Documentation](#https://docs.python.org/3/contents.html)
- [Main()](#main())
  - [__ main __](#main)
  <!-- - https://docs.python.org/3/library/index.html
  - https://docs.python.org/3/reference/index.html
  - https://docs.python.org/3/howto/index.html
  - https://docs.python.org/3/reference/import.
  - html#replacing-the-standard-import-system -->
- [Executing modules as scripts](#)
- [Options Command](#)
- [`-c` command](#)
<!-- - [`-m` module-name](#) https://realpython.com/run-python-scripts/ -->
- Language limitations
  - GIL
- Python Files
  - [.py](#Files:-.)
  - [.pyc](#Files:-.)
  - [.pyo](#Files:-.)
  - [.egg](#Files:-.)
  - [`__init__.py`](#_init.py)
  - [`__main__.py`](#_main.py)
  - [Requirements File](#requirements-file)
  - [Pipfile and Pipfile.lock](#pipfile-and-pipfile.lock)

<!-- ## Advanced
- [Anonymous functions (lambda)](https://pt.stackoverflow.com/questions/50422/como-declarar-uma-fun%C3%A7%C3%A3o-an%C3%B4nima-no-python)
- Generators
- Iterators
- Decorators
- Personal Exceptions
- Enfeites em funções
- Metaclasses
- coroutine function
- concurrent

## Build, Distribute and Deploy Python Code
This part of the guide focuses on sharing and deploying your Python code.
- https://docs.python-guide.org/ -->


## Best Pratices
- [Identation and Length](#identation-and-length)
- [Line Break After a Binary Operator](#line-break-after-a-binary-operator)
- [Naming](#naming)
- [Encoding](#encoding)
- [Strings `' '` and `" "`](#strings-and)
- [Comments `#`](#comments)
- [Imports](#imports)
- [Dunders to Documentation](#dunders-to-documentation)
- [Annotation Functions](#annotation-functions)
 - [Type Hints](#type-hints)
- [String Concatenation](#string-concatenation)
- [String Methods](#string-methods)
- [Exception](#exception)
- [Return](#return)
- [Type Comparisons](#type-comparisons)
- [Methods with numerous parameters ](#methods-with-numerous-parameters)
- Docstrings
    - [`__doc__`](#__doc__)
    - [`help()`](#help)
    - [Scripts with docstrings](#scripts-with-docstrings)
    - [Functions with Docstrings](#functions-with-docstrings)
    - [Class with Docstrings](#class-with-docstrings)
<!-- TODO - https://realpython.com/documenting-python-code/
TODO - https://docs.python-guide.org/ -->

<!-- 
# **Awesome Python**

- [Functional Programming](#functional-programming)
- [Package Management](#package-management)
- [Package Repositories](#package-repositories)

**Managemant Libraries**
- [Python Package Index](https://pypi.org/)
- [Poetry](https://python-poetry.org/)
- [Conda](https://docs.conda.io/en/latest/)
- [Pipenv](https://pipenv-fork.readthedocs.io/en/latest/) -->


---


## Interpreter and Compiler


### CPython
Compiler and interpreter bytecode, write in C.

### Jython
<img src="images/jython.jpg"   align="center" height=auto width=50% />

Compiler and interpreter Java bytecode, write in Java.


### Comparian

<img src="images/comp-interpreter.png"  align="center" height=auto width=80%/>

#### Why use alter compiler python?

**CPython:** torna muito fácil escrever extensões C para seu código Python porque no final ele é executado por um interpretador C. <br/>
**Jython:**, por outro lado, torna muito fácil trabalhar com outros programas Java: você pode importar qualquer classe Java sem esforço adicional, chamando e utilizando suas classes Java de dentro de seus programas Jython.


#### How Python program run ?

<img src="images/interpreter.png"  align="center" height=auto width=100%/>

1. First, Python interpreter **checks syntax** (sequential)
2. **Compile and convert it to bytecode** and directly bytecode is loaded in system memory.
3. Then compiled bytecode interpreted from memory to execute it.

---

## Programming Recommendations

_"Readability counts"_

##### Identation and Length
- 4 spaces
- Limit all line 72 characteres to docstring
- Limit all line 79 to code
- Statement of functions and flow, e.g:

```Python
# Aligned with opening delimiter.
foo = long_function_name(var_one=0.0, var_two=0.0,
                         var_three=0.0, var_four=0.0)

```

##### Naming
- Class Name (camelCase): `CapWords()`
- Variables (snack_case): `cat_words`
- Constants: `MAX_OVERFLOW`


##### Line Break After a Binary Operator
```Python
income = (gross_wages
          + taxable_interest
          + (dividends - qualified_dividends)
          - ira_deduction
          - student_loan_interest)

```

##### Encoding
By default: `UTF-8`

```Python
# -*- coding: UTF-8 -*-
<code>
```

##### Strings `' '` and `" "`
Single quotation marks and strings with double quotation marks are the same.

##### Comments `#`
- Fisrt word **need** upper case.
- Comments in-line separete by 2 spaces.
```Python
x = x + 1  # Compensar borda
```

##### Imports
Following order:

1. Standard library imports.
2. Related third party imports.
(_parte de terceiros_)
3. Local application/library specific imports.

```Python
import argparse
import configparser
import os

import mysql.connector

import my_module
```

Yes:
```Python
import os
import sys
```

No:
```Python
import os, sys
```

No problems:
```Python
from subprocess import Popen, PIPE
```


##### Dunders to Documentation
```Python
__version__ = '0.1'
__author__ = 'Bruno Campos'
```


##### String Concatenation

- Use ` ''.join()`, to concatenate 3 or more:
```python
os.path.dirname.join(stringA + stringB + stringC + stringD)
```

- This optimization is fragile even in CPython. **Not** use:
```python
stringA + stringB + stringC + stringD
```


##### String Methods

- Use string methods instead of the string module because, String methods are always much faster.
- Use `''.startswith()` and `''.endswith()` instead of string slicing to check for prefixes or suffixes.

```Python
Yes: if foo.startswith('bar'):
No:  if foo[:3] == 'bar':
```


##### Exception

Limit the clausule `try:` minimal code necessary.

Yes:
```Python
try:
    value = collection[key]
except KeyError:
    return key_not_found(key)
else:
    return handle_value(value)
```

No:
```Python
try:
    # Too broad!
    return handle_value(collection[key])
except KeyError:
    # Will also catch KeyError raised by handle_value()
    return key_not_found(key)
```

- Objetivo de responder à pergunta **"O que deu errado?"** programaticamente, em vez de apenas afirmar que _"Ocorreu um problema"_


##### Return
"_Should explicitly state this as return None_"

- Be consistent in return statements.
- Todas as instruções de retorno em uma função devem retornar uma expressão ou nenhuma delas deve.

Yes:
```Python
def foo(x):
    if x >= 0:
        return math.sqrt(x)
    else:
        return None
```

No:
```Python
def foo(x):
    if x >= 0:
        return math.sqrt(x)
```


##### Type Comparisons
- Always use `isinstance()`
```Python
Yes: if isinstance(obj, int):

No:  if type(obj) is type(1):
```

#### Annotation Functions
"_Don’t use comments to specify a type, when you can use type annotation._"

-  Atua como um linter (analisador de código para mostrar erros) muito poderoso.
- O Python não atribui nenhum significado a essas anotações.
- _Examples_:

Method arguments and return values
```Python
def func(a: int) -> List[int]:
```

```Python
def hello_name(name: str) -> str:
    return (f'Hello' {name}')
```

Declare the type of a variable (type hints)
```python
a = SomeFunc()  # type: SomeType
```

Isso informa que o tipo esperado do argumento de nome é str . Analogicamente, o tipo de retorno esperado é str .

##### Type Hints
```Python
def send_email(address,     # type: Union[str, List[str]]
               sender,      # type: str
               cc,          # type: Optional[List[str]]
               bcc,         # type: Optional[List[str]]
               subject='',
               body=None    # type: List[str]
               ):
    """Send an email message.  Return True if successful."""
    <code>
```

TODO
- https://docs.python.org/3/library/typing.html#module-typing


##### References
- https://medium.com/@shamir.stav_83310/the-other-great-benefit-of-python-type-annotations-896c7d077c6b
- https://www.python.org/dev/peps/pep-0484/
- https://blog.jetbrains.com/pycharm/2015/11/python-3-5-type-hinting-in-pycharm-5/

---

## Docstrings

- Docstrings must have:
  - Args
  - Returns
  - Raises

Simple Example
```Python
def say_hello(name):
    """
    A simple function that says hello...
    Richie style
    """

    print(f"Hello {name}, is it me you're looking for?")
```

Example partner Google
```Python
def fetch_bigtable_rows(big_table, keys, other_silly_variable=None):
    """Fetches rows from a Bigtable.

    Retrieves rows pertaining to the given keys from the Table instance
    represented by big_table.  Silly things may happen if
    other_silly_variable is not None.

    Args:
        big_table: An open Bigtable Table instance.
        keys: A sequence of strings representing the key of each table row
            to fetch.
        other_silly_variable: Another optional variable, that has a much
            longer name than the other args, and which does nothing.

    Returns:
        A dict mapping keys to the corresponding table row data
        fetched. Each row is represented as a tuple of strings. For
        example:

        {'Serak': ('Rigel VII', 'Preparer'),
         'Zim': ('Irk', 'Invader'),
         'Lrrr': ('Omicron Persei 8', 'Emperor')}

        If a key from the keys argument is missing from the dictionary,
        then that row was not found in the table.

    Raises:
        IOError: An error occurred accessing the bigtable.Table object.
    """
    return None
```

#### `__doc__`

Such a docstring becomes the `__doc__` special attribute of that object.

- Simple Example
```Python
print(say_hello.__doc__)

# A simple function that says hello... Richie style
```

- Example partner Google

<img src='images/__doc__.png' align="center" height=auto width=1000%>


##### `help()`
- Create manual: `man`
- Is a built-in function help() that prints out the objects docstring.

```Python
>>> help(say_hello)
Help on function say_hello in module __main__:

# say_hello(name)
#     A simple function that says hello... Richie style
```

<img src='images/help().png'>

##### Scripts with Docstrings
- Docstrings must show how to use script
- Must doc:
  - Usage: sintax command line
  - Examples
  - Arguments required and optional

```python
"""
Example of program with many options using docopt.
Usage:
  options_example.py [-hvqrf FILE PATH]
  my_program tcp <host> <port> [--timeout=<seconds>]

Examples:
  calculator_example.py 1 + 2 + 3 + 4 + 5
  calculator_example.py 1 + 2 '*' 3 / 4 - 5    # note quotes around '*'
  calculator_example.py sum 10 , 20 , 30 , 40

Arguments:
  FILE     input file
  PATH     out directory

Options:
  -h --help            show this help message and exit
  --version            show version and exit
  -v --verbose         print status messages
  -q --quiet           quiet mode
  -f --force
  -t, --timeout TIMEOUT    set timeout TIMEOUT seconds
  -a, --all             List everything.

"""
from docopt import docopt


if __name__ == '__main__':
    arguments = docopt(__doc__, version='1.0.0rc2')
    print(arguments)
```

##### Functions with Docstrings
A docstring to a function or method must resume:
- behavior
- arguments required
- arguments optional
- default value of arguments
- returns
- raise Exceptions

Example

```Python
def says(self, sound=None):
    """Prints what the animals name is and what sound it makes.

    If the argument `sound` isn't passed in, the default Animal
    sound is used.

    Parameters
    ----------
    sound : str, optional
        The sound the animal makes (default is None)

    Raises
    ------
    NotImplementedError
        If no sound is set for the animal or passed in as a parameter.
    """

    if self.sound is None and sound is None:
        raise NotImplementedError("Silent Animals are not supported!")

    out_sound = self.sound if sound is None else sound
    print(self.says_str.format(name=self.name, sound=out_sound))

```

##### Class with Docstrings
A docstring para uma classe deve resumir seu comportamento e listar os métodos públicos e variáveis ​​de instância. Se a classe se destina a ser uma subclasse e possui uma interface adicional para subclasses, essa interface deve ser listada separadamente (no docstring). O construtor de classe deve ser documentado na docstring para seu método __init__ . Os métodos individuais devem ser documentados por seus próprios docstring.

Example
```Python
class SimpleClass:
    """Class docstrings go here."""

    def say_hello(self, name: str):
        """Class method docstrings go here."""

        print(f'Hello {name}')
```

Class docstrings should contain the following information:

- A brief summary of its purpose and behavior
- Any public methods, along with a brief description
- Any class properties (attributes)
- Anything related to the interface for subclassers, if the class is intended to be subclassed



##### References
- [PEP 08](https://www.python.org/dev/peps/pep-0008/)
- [PEP 484](https://www.python.org/dev/peps/pep-0484/)
- [PEP 257](https://www.python.org/dev/peps/pep-0257/)
- https://realpython.com/python-pep8/#naming-conventions
- https://pep8.org
- Style guide Google: https://github.com/google/styleguide/blob/gh-pages/pyguide.md#38-comments-and-docstrings

#### Methods with numerous parameters
Methods with numerous parameters are a challenge to maintain, especially if most of them share the same datatype.
<br/>
These situations usually denote the **need for new objects to wrap the
 numerous parameters**.


#### Example(s):

- too many arguments
```python
def add_person(birthYear: int, birthMonth: int, birthDate: int,
               height: int, weight: int,
               ssn: int):
'''too many arguments'''

    . . .
```
- preferred approach
```python
def add_person(birthdate: 'Date',
               measurements: 'BodyMeasurements',
               ssn: int):
'''preferred approach'''

    . . .
```


## Cyclomatic Complexity
cyclomatic complexity counts the number of decision points in a method

---

# Basic Comands
- Libraries
- Function print
- Types data
- Numeric systems
- libs matematics


## Control Structure
- Conditional
- Repeatition
- Functional Programming

## Simple Data Structure
 - Tuples
 - List
 - Dict

## Functions
- Defining Functions
- Documentation
- Default arguments
- Packing and unpacking arguments
- Variable Scope
- Global variable
- Constants
- function recursive
- Lambda Expressions

```
 Do global variables evil?

 global variables are bad in any programming language.

 However, global constants are not conceptually the same as global variables;
 global constants are perfectly fine to use.

 so when you need a constant you have to use a global.

 - http://wiki.c2.com/?GlobalVariablesAreBad


 To make code more modular, the first step is always to move all global variables into a "config" object.

```
#### Violating Pure Function definition
I believe that a clean and (nearly) bug-free code should have functions that are as pure as possible (see pure functions). A pure function is the one that has the following conditions:

A função sempre avalia o mesmo valor de resultado, dado o (s) mesmo (s) valor (es) do argumento. O valor do resultado da função não pode depender de qualquer informação ou estado oculto que possa mudar enquanto a execução do programa prossegue ou entre diferentes execuções do programa, nem pode depender de qualquer entrada externa de dispositivos de E / S (normalmente - veja abaixo).
A avaliação do resultado não causa nenhum efeito colateral observável semanticamente, como a mutação de objetos mutáveis ​​ou a saída para dispositivos de E / S.
Ter variáveis ​​globais está violando pelo menos um dos itens acima, se não ambos, pois um código externo provavelmente pode causar resultados inesperados.

Outra definição clara de funções puras: "Função pura é uma função que toma todas as suas entradas como argumentos explícitos e produz todas as suas saídas como resultados explícitos". [1] Ter variáveis ​​globais viola a idéia de funções puras, já que uma entrada e talvez uma das saídas (a variável global) não está sendo explicitamente dada ou retornada.


#### Violating Unit testing F.I.R.S.T principle
Further on that, if you consider unit-testing and the F.I.R.S.T
 principle (Fast tests, Independent tests, Repeatable, Self-Validating and Timely) will probably violate the Independent tests principle (which means that tests don't depend on each other).




#### Using built-in data structure
Use dictionary, ex:<br/>
```bash
DATABASE_CONFIG = {
    'host': 'localhost',
    'dbname': 'company',
    'user': 'user',
    'password': 'password',
    'port': 3306
}
```
<br/>
Must is file separed, how example `config.py`


#### Using environment variables
The configuration values are not managed as a separate file.

## Control Flow
-  examples
  - [range](https://docs.python.org/3/library/stdtypes.html#range)
  - Looping Techniques
    - items()
    - enumerate()
    - zip()

###### items()
- dictionaries

```python
knights = {'gallahad': 'the pure',
           'robin': 'the brave'}

for k, v in knights.items():
     print(k, v)

# gallahad the pure
# robin the brave
```

###### enumerate()
- List

```python
for i, v in enumerate(['tic', 'tac', 'toe']):
    print(i, v)

# 0 tic
# 1 tac
# 2 toe
```

###### zip()
- Loop over two or more sequences at the same time
- Excelent tools to garant good algorith complex

```python
questions = ['name', 'quest', 'favorite color']
answers = ['lancelot', 'the holy grail', 'blue']


for q, a in zip(questions, answers):
    print('What is your {0}?  It is {1}.'.format(q, a))

# What is your name?  It is lancelot.
# What is your quest?  It is the holy grail.
# What is your favorite color?  It is blue.
```




## Functions

TODO:
- https://nbviewer.jupyter.org/github/ricardoduarte/python-for-developers/blob/master/Chapter6/Chapter6_Functions.ipynb

- examples
- Optional arguments
- Unpacking Argument (**kwargs)


##### Optional arguments

```python
def parrot(voltage, state='a stiff', action='voom', type='Norwegian Blue'):
```
Accepts **one required argument (`voltage`)** and three optional arguments (`state, action, and type`)

##### Unpacking Argument
```python
def parrot(voltage, state='a stiff', action='voom'):
    print("-- This parrot wouldn't", action, end=' ')
    print("if you put", voltage, "volts through it.", end=' ')
    print("E's", state, "!")

d = {"voltage": "four million",
     "state": "bleedin' demised",
     "action": "VOOM"}

parrot(**d)

# This parrot wouldn't VOOM if you put four million volts through it. E's bleedin' demised !
```


<!-- ## Exceptions
TODO

## Strings
TODO:
- https://nbviewer.jupyter.org/github/ricardoduarte/python-for-developers/blob/master/Chapter5/Chapter5_Types.ipynb

```
 +---+---+---+---+---+---+
 | P | y | t | h | o | n |
 +---+---+---+---+---+---+
 0   1   2   3   4   5   6
-6  -5  -4  -3  -2  -1
```

```
print('The story of {0}, {1}, and {other}.'.format('Bill', 'Manfred',
                                                       other='Georg'))
# The story of Bill, Manfred, and Georg.
``` -->

## Files
- o arquivo de saída padrão pode ser referenciado como `sys.stdout`

## Serialization
- Pickle
- sqlite

## Classes
- Um namespace é um mapeamento de nomes para objetos.
apenas ligam nomes a objetos
- verbos para métodos e substantivos para atributos de dados
-  nada no Python torna possível impor a ocultação de dados

Examples:
```python
class MyClass:
    """A simple example class"""
    i = 12345

    def f(self):
        return 'hello world'
```
##### self
- O primeiro argumento de um método é chamado self. Isso nada mais é do que uma convenção
- É útil para aumenta a legibilidade dos métodos: não há chance de confundir variáveis ​​locais e variáveis ​​de instância ao olhar através de um método.

```python
class Bag:
    def __init__(self):
        self.data = []

    def add(self, x):
        self.data.append(x)

    def addtwice(self, x):
        self.add(x)
        self.add(x)
```

##### `__class__`
- Each value is an object. It is stored as `object.__class__`

```python
class MyFirstClass:
    """A simple example class"""
    i = 42

    def func_ex(self):
        print('learning Python')


if __name__ == '__main__':
    object = MyFirstClass()  # initialized instance
    object.func_ex()

    print(object.__class__)

# learning Python
# <class '__main__.MyFirstClass'>
```

<!-- ##### Inheritance


##### Private Variables

##### Iterators
When call `for` the interpreter call `iter()`<br/>
The function `iter()` return next object of list

##### Generators

##### Generators Expressoins
`sum(i*i for i in range(10))                 # sum of squares`

## Tests
One approach for developing high quality software is to write tests for each function



#### doctest
The doctest module provides a tool for scanning a module and validating tests embedded in a program’s docstrings.
<br/>
Isso aprimora a documentação fornecendo ao usuário um exemplo e permite que o módulo doctest verifique se o código permanece fiel à documentação:
```python
def average(values):
    """Computes the arithmetic mean of a list of numbers.

    >>> print(average([20, 30, 70]))
    40.0
    """
    return sum(values) / len(values)

import doctest
doctest.testmod()   # automatically validate the embedded tests
```

...

## Logging
```
import logging
logging.debug('Debugging information')
logging.info('Informational message')
logging.warning('Warning:config file %s not found', 'server.conf')
logging.error('Error occurred')
logging.critical('Critical error -- shutting down')
```
...

### stdin, stdout, and stderr

## Threads
...

## Web
- Scrapping

### Frameworks
- Flask (microframework)
- Django

# Orientação à objetos
...

# Design Pattern
...

## Science
- Numpy
- Pandas
- Matplotlib
- Skitlearn (aprendizagem supervisionada, nao supervisionada)
- TensorFlow (neural network) -->

---


## References
- https://realpython.com/python-virtual-environments-a-primer/
- https://github.com/vinta/awesome-python/edit/master/README.md
- https://www.digitalocean.com/community/tutorials/how-to-install-python-3-and-set-up-a-programming-environment-on-ubuntu-18-04-quickstart
- https://jtemporal.com/requirements-txt/
- https://pip.pypa.io/en/stable/user_guide/

---

<p  align="left">
<br/>
<a href="mailto:brunocampos01@gmail.com" target="_blank"><img src="https://github.com/brunocampos01/devops/blob/master/images/email.png" alt="Gmail" width="30">
</a>
<a href="https://stackoverflow.com/users/8329698/bruno-campos" target="_blank"><img src="https://github.com/brunocampos01/devops/blob/master/images/stackoverflow.png" alt="GitHub" width="30">
</a>
<a href="https://www.linkedin.com/in/brunocampos01" target="_blank"><img src="https://github.com/brunocampos01/devops/blob/master/images/linkedin.png" alt="LinkedIn" width="30"></a>
<a href="https://github.com/brunocampos01" target="_blank"><img src="https://github.com/brunocampos01/devops/blob/master/images/github.png" alt="GitHub" width="30"></a>
<a href="https://brunocampos01.netlify.app/" target="_blank"><img src="https://github.com/brunocampos01/devops/blob/master/images/blog.png" alt="Website" width="30">
</a>
<a href="https://medium.com/@brunocampos01" target="_blank"><img src="https://github.com/brunocampos01/devops/blob/master/images/medium.png" alt="GitHub" width="30">
</a>
<a rel="license" href="http://creativecommons.org/licenses/by-sa/4.0/"><img alt="Creative Commons License" style="border-width:0" src="https://i.creativecommons.org/l/by-sa/4.0/88x31.png",  align="right" /></a><br/>
</p>
