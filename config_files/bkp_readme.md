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

<!-- 
# **Awesome Python**

- [Functional Programming](#functional-programming)
- [Package Management](#package-management)
- [Package Repositories](#package-repositories)


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
