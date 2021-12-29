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

<br/>
**Curso em Vídeo: resolutions exercises**
<br/>
- Learning Python in portuguese !
- Class notes and exercises solved
- Teacher: Gustavo Guanabara.

Words   | Themes
------- | ---
1 | [Fundamentals](https://www.youtube.com/playlist?list=PLHz_AreHm4dlKP6QQCekuIPky1CiwmdI6)
2 | [Control Structures](https://www.youtube.com/playlist?list=PLHz_AreHm4dk_nZHmxxf_J0WRAqy5Czye)
3 | [Compound Structures](https://www.youtube.com/watch?v=0LB3FSfjvao&list=PLHz_AreHm4dksnH2jVTIVNviIMBVYyFnH)
4 | [Functions](https://www.youtube.com/watch?v=0LB3FSfjvao&list=PLHz_AreHm4dksnH2jVTIVNviIMBVYyFnH)


### FAQ
- How do I configure my computer to run Python code?
- How do I configure my computer to develop in Python?
- What are the best practices to prepare an environment that runs Python?
- What is a requirements.txt file ?
- How to ensure a fully reproducible (100% equal) environment ?
- How is the virtual environment Python executable able to use something different from the system site packages ?
- When use golang in place Python
---
---

## How to install and set up a Python
<img src='images/config.jpg'  align="center" height=280 width=100%>

On **Linux**, make sure you have the right version of Python pre-installed, and the basic developer toolset available. Makes sure of that:

1. Install the latest version of Python.
```bash
sudo apt install python3.8
```

2. Satisfy some system requirements
```bash
sudo apt install build-essential\
                 libffi-dev\
                 python3-pip\
                 python3-dev\
                 python3-venv \
                 python3-setuptools\
                 python3-pkg-resources
```

2. Create and activate Python virtual environment

```bash
cd your-project
python3 -m venv venv
source venv/bin/activate
```

NOTE for beginners:
<br/>
A Python virtual environment is a local interpreter that allows to install dependencies without polluting the global Python interpreter. There are different ways to create virtual environments (virtualenv; -m venv) and to install packages (pip install; easy_install), which may be confusing at the beginning.


4. Install tools
- [Git](https://github.com/brunocampos01/devops/tree/master/git)
```bash
sudo apt install git
```

- Vim editor (git's default editor)
```bash
sudo apt install vim
```

5. Install Libraries used in this project
```bash
pip3 install --user od \
                    numpy \
                    pandas \
                    matplotlib \
                    virtualenv \
                    jupyter \
                    mysql-connector-python
```

---


## Check Python Configuration

<img src='images/Python3VersionChange.jpg' width="80%">

- Check what version Python
```bash
python --version

# Python 3.6.7
```

If return Python2, try set a alias in file [.bashrc](https://github.com/brunocampos01/home-sweet-home/blob/master/.bashrc)
```
# Python
alias python=python3
```

- Check **where** installed Python
```bash
which python

# /usr/bin/python
```

---

## Preparing Environment

### Enviornment Variables

- To individual project
`PYTHONPATH` search path until module.

- To interpreter
`PYTHONHOME` indicate standard libraries.

### Configure Python PATH
1. First open profile in editor
```bash
sudo vim ~/.profile
```

or

```bash
sudo vim ~/.bashrc
```

2. Insert Python PATH
```bash
export PYTHONHOME=/usr/bin/python<NUMER_VERSION>
```

<img src='images/bashrc_python.png'  align="center" height=auto width=50%>

NOTE: quit vim: `ESC, :wq`


3. Update profile/bashrc
```bash
source ~/.bashrc

# or

.  ~/.bashrc
```

### Install multiple Python3
`update-alternatives` symbolic links determining default commands

1. Execute in terminal
```bash
sudo update-alternatives --config python
```
If return error: `update-alternatives: error: no alternatives for python3`, following to step [2](#2)

2. Install multiples Python
```bash
update-alternatives --install /usr/bin/python python /usr/bin/python<NUMER_VERSION> 1

update-alternatives --install /usr/bin/python python /usr/bin/python<OTHER_NUMER_VERSION> 2
```

3. Change Python versions
```bash
sudo update-alternatives --config python
```

<img src="images/python_alternatives.png" width="1000" />

```bash
sudo update-alternatives  --set python /usr/bin/python3.6
```

4. Check changes
```bash
python --version

# Python 3.8
```

---

## Requirements File
_Requirements files_ is file containing a list of items to be installed using pip install.

- Generate file `requirements.txt`
```bash
pip3 freeze > requirements.txt
```

or

```bash
venv/bin/pip3 freeze > requirements.txt
cat requirements # image bellow
```
<img src="images/requeriments.png" align="center" height=auto width=50%/>


- Visualize instaled libraries
```bash
pip3 freeze
```
<img src="images/freeze.png" align="center" height=auto width=100%/>

- Install libraries in requirements
```bash
pip3 install -r requirements.txt
```
`-r` recursive

---

## Virtual Environment
<img src="images/virtual_env_p3.png"  align="center" height=auto width=80%/>

The Python can is executed in a virtual environment with **semi-isolated** from system.
<br/>
When Python is initiating, it analyzes the path of its binary. In a virtual environment, it's actually just a copy or Symbolic link to your system's Python binary. Next, set the `sys.prefix` location which is used to locate the `site-packages` (third party libraries)

_Quando o Python está iniciando, ele analisa o caminho do seu binário. Em um virtual environment, na verdade, é apenas uma cópia ou Symbolic link para o binário Python do seu sistema. Em seguida, define o local `sys.prefix` que é usado para localizar o `site-packages`(third party libraries)._

<img src="images/venv.png"  align="center" height=auto width=80%/>

### Symbolic link
- `sys.prefix` points to the virtual environment directory.
- `sys.base.prefix` points to the **non-virtual** environment.

Example, how keep the files in folder of virtual environment:
```bash
ll

# random.py -> /usr/lib/python3.6/random.py
# reprlib.py -> /usr/lib/python3.6/reprlib.py
# re.py -> /usr/lib/python3.6/re.py
# ...
```

```bash
tree

├── bin
│   ├── activate
│   ├── activate.csh
│   ├── activate.fish
│   ├── easy_install
│   ├── easy_install-3.8
│   ├── pip
│   ├── pip3
│   ├── pip3.8
│   ├── python -> python3.8
│   ├── python3 -> python3.8
│   └── python3.8 -> /Library/Frameworks/Python.framework/Versions/3.8/bin/python3.8
├── include
├── lib
│   └── python3.8
│       └── site-packages
└── pyvenv.cfg
```

### Create Virtual Environment
```bash
$ virtualenv -p python3  NAME_ENVIRONMENT
(env) $
```
or
```bash
$ python3 -m venv NAME_ENVIRONMENT
(env) $
```

###  To begin using the virtual environment, it needs to be activated
<img src="images/virtualenv.gif" align="center" height=auto width=100%/>

Execute activate script
```bash
source <DIR>/bin/activate
```

<img src="images/env.png" align="center" height=auto width=100%/>


#### References
- [python-virtual-environments-a-primer](https://realpython.com/python-virtual-environments-a-primer/)

---

## Pipenv
- Package manager: `Pipefile`
- Virtual environment: `$HOME/.local/share`
- Lock package: `Pipefile.lock`

<img src="images/pipe.gif" align="center" height=auto width=100%/>


### Why use pipefile?
Using pip and requirements.txt file, have a **real issue here is that the build isn’t [deterministic](https://pt.wikipedia.org/wiki/Algoritmo_determin%C3%ADstico)**. What I mean by that is that, given the same input (the requirements.txt file), pip doesn’t always produce the same environment.

### What is pipefile?
It automatically creates and manages a virtualenv for your projects, as well as adds/removes packages from your Pipfile as you install/uninstall packages. It also generates the ever-important Pipfile.lock, which is used to produce deterministic builds.

Features:
- Deterministic builds
- Separates development and production environment libraries into a single file `Pipefile`
- Automatically adds/removes packages from your `Pipfile`
- Automatically create and manage a virtualenv
- Check PEP 508 requirements
- Check installed package safety

### Comparisons
```
# Pipfile

[[source]]
name = "pypi"
url = "https://pypi.org/simple"
verify_ssl = true

[dev-packages]
matplotlib = "==3.1.3"

[packages]
requests = "*"
numpy = "==1.18.1"
pandas = "==1.0.1"
wget = "==3.2"

[requires]
python_version = "3.8"
platform_system = 'Linux'
```

```
# requirements.txt

requests
matplotlib==3.1.3
numpy==1.18.1
pandas==1.0.1
wget==3.2
```


### Install
```bash
pip3 install --user pipenv
```

### Create Pipfile and virtual environment
```bash
pipenv --python 3

# Creating a virtualenv for this project…
# Pipfile: /home/campos/projects/becoming-a-expert-python/Pipfile

# Using /usr/bin/python3.8 (3.8.2) to create virtualenv…
# ⠼ Creating virtual environment...created virtual environment CPython3.8.2.final.0-64 in 256ms

#   creator CPython3Posix(dest=/home/campos/.local/share/virtualenvs/becoming-a-expert-python-fmPL6zJP, clear=False, global=False)

#   seeder FromAppData(download=False, pip=latest, setuptools=latest, wheel=latest, via=copy, app_data_dir=/home/campos/.local/share/virtualenv/seed-app-data/v1)

#   activators BashActivator,CShellActivator,FishActivator,PowerShellActivator,PythonActivator,XonshActivator

# ✔ Successfully created virtual environment!
# Virtualenv location: /home/campos/.local/share/virtualenvs/becoming-a-expert-python-fmPL6zJP

# requirements.txt found, instead of Pipfile! Converting…
# ✔ Success!
```

- See where virtual environment installed
```bash
pipenv --venv
```

### Activate environment
```bash
pipenv run
```
<img src='images/pipenv.png' width="100%">

### Install Libraries with Pipefile
```bash
pipenv install flask

# or

pipenv install --dev flask
```

### Create lock file
```bash
pipenv lock

# Locking [dev-packages] dependencies…
# Locking [packages] dependencies…
# ✔ Success!
```

#### References
- [Official documentation](https://github.com/pypa/pipenv)
- [Gerenciando suas dependências e ambientes python com pipenv](https://medium.com/code-rocket-blog/gerenciando-suas-depend%C3%AAncias-e-ambientes-python-com-pipenv-9e5413513fa6)
- [How are Pipfile and Pipfile.lock used?](https://stackoverflow.com/questions/46330327/how-are-pipfile-and-pipfile-lock-used)

---


## Simple Deterministic Build

```
pip install pip-tools
pip3 freeze > requirements.in

pip-compile --generate-hashes requirements.in
```

output: requirements.txt
```
wtforms==2.3.3 \
    --hash=sha256:7b504fc724d0d1d4d5d5c114e778ec88c37ea53144683e084215eed5155ada4c \
    --hash=sha256:81195de0ac94fbc8368abbaf9197b88c4f3ffd6c2719b5bf5fc9da744f3d829c
    # via
    #   -r requirements.in
    #   flask-admin
    #   flask-wtf
zict==2.0.0 \
    --hash=sha256:26aa1adda8250a78dfc6a78d200bfb2ea43a34752cf58980bca75dde0ba0c6e9 \
    --hash=sha256:8e2969797627c8a663575c2fc6fcb53a05e37cdb83ee65f341fc6e0c3d0ced16
    # via
    #   -r requirements.in
    #   distributed
zipp==3.4.0 \
    --hash=sha256:102c24ef8f171fd729d46599845e95c7ab894a4cf45f5de11a44cc7444fb1108 \
    --hash=sha256:ed5eee1974372595f9e416cc7bbeeb12335201d8081ca8a0743c954d4446e5cb
    # via
    #   -r requirements.in
    #   importlib-metadata
    #   importlib-resources
    #   pep517
```












---
<!-- 
## Python Files
REFACTORING
https://packaging.python.org/key_projects/#pipenv

In production ...
- distlib
- virtualenv
- eggs
- Wheel

#### Files: `.py`

File: Typically, a Python file is any file that contains code. Most Python files have the extension .py.

Script: A Python script is a file that you intend to execute from the command line to accomplish a task.

Module: A Python module is a file that you intend to import from within another module or a script, or from the interactive interpreter. You can read more about modules in the Python documentation.


Call unique def in file.py (`python -c "import FILE_NAME; def test(requirements)"`)



```
sound/                          Top-level package
      __init__.py               Initialize the sound package
      formats/                  Subpackage for file format conversions
              __init__.py
              wavread.py
              wavwrite.py
              aiffread.py
              aiffwrite.py
              auread.py
              auwrite.py
              ...
      effects/                  Subpackage for sound effects
              __init__.py
              echo.py
              surround.py
              reverse.py
              ...
      filters/                  Subpackage for filters
              __init__.py
              equalizer.py
              vocoder.py
              karaoke.py
              ...

```

#### `__init__.py`

- The `__init__.py` files are required to make Python treat directories containing the file as packages.
- File can empty
- Is good pratice `__init__` have a list with modules to import. Example:
```
__all__ = ["echo", "surround", "reverse"]
```
- So import `from sound.effects import *` call the modules: "echo", "surround", "reverse"


Import individual module:<br/>
```python
from package import item.subitem.subsubite...

from module import name
```

TODO:
- https://nbviewer.jupyter.org/github/ricardoduarte/python-for-developers/blob/master/Chapter10/Chapter10_Packages.ipynb


#### Global Modules
- Módulos que são projetados para uso via M import * devem usar o mecanismo `__ all __` para impedir a exportação de globals

- To better  support introspection
Use __ all __ to switch *. E.g
```Python
__all__ = ['foo', 'Bar']

from module import *
```
significa que, quando você `from module import * ` apenas esses nomes __all__ são importados.

EXAMPLES...
- More details: https://stackoverflow.com/questions/44834/can-someone-explain-all-in-python and https://www.python.org/dev/peps/pep-0008/#naming-conventions



- Examples ...
- Read: https://realpython.com/run-python-scripts/


#### Compiler Files: `.pyc`
Program **doesn’t run any faster when it is read from a .pyc** file than when it is read from a .py file;

.pyc it's faster to loaded modules -->

---

## Undertanding

### Zen of Python

<img src="images/zen.png" align="center" height=auto width=80%/>

```python
Beautiful is better than ugly.
Explicit is better than implicit.
Simple is better than complex.
Complex is better than complicated.
Flat is better than nested.
Sparse is better than dense.
Readability counts.
Special cases aren't special enough to break the rules.
Although practicality beats purity.
Errors should never pass silently.
Unless explicitly silenced.
In the face of ambiguity, refuse the temptation to guess.
There should be one-- and preferably only one --obvious way to do it.
Although that way may not be obvious at first unless you're Dutch.
Now is better than never.
Although never is often better than *right* now.
If the implementation is hard to explain, it's a bad idea.
If the implementation is easy to explain, it may be a good idea.
Namespaces are one honking great idea -- let's do more of those!
```

NOTE: [PEP 20](https://www.python.org/dev/peps/pep-0020/)

---

## Types

<img src="images/Python_3._The_standard_type_hierarchy.png" width="1000" />

Examples:
```python
# Converting real to integer
print 'int(3.14) =', int(3.14)

# Converting integer to real
print 'float(5) =', float(5)

# Calculation between integer and real results in real
print '5.0 / 2 + 3 = ', 5.0 / 2 + 3

# Integers in other base
print "int('20', 8) =", int('20', 8) # base 8
print "int('20', 16) =", int('20', 16) # base 16

# Operations with complex numbers
c = 3 + 4j
print 'c =', c
print 'Real Part:', c.real
print 'Imaginary Part:', c.imag
print 'Conjugate:', c.conjugate()

# int(3.14) = 3
# float(5) = 5.0
# 5.0 / 2 + 3 =  5.5
# int('20', 8) = 16
# int('20', 16) = 32
# c = (3+4j)
# Real Part: 3.0
# Imaginary Part: 4.0
# Conjugate: (3-4j)
```

---
## Interpreter and Compiler

 <img src="images/cpython.png"  align="center" height=auto width=80% />

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


## Configuration File
There are ways to manage the configuration:
- Using built-in data structure
- Using external configuration file
    - json
    - ini
- Using environment variables
- Using dynamic loading


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
