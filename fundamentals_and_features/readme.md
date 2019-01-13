# Fundamentals and Features Language
- Pre Requeriments
- Python PATH
- How alter Python PATH and Python version
- Change versions of python
- What is Python?
- Zen of Python
- Keys words
- Types
- Interpreter Python
- How Python program run
- Environment Virtual
- PEP 8:   https://realpython.com/python-pep8/#naming-conventions


## Pre Requeriments
- Vim editor:<br/>
`sudo apt install vim`
- Python 3.7 or more:<br/>
`sudo apt install python3.7`
- Git:<br/>
`sudo apt get install git`
- pip:<br/>
`sudo apt install python-pip`
- Jupyter Notebook:<br/>
`sudo wget https://repo.anaconda.com/archive/Anaconda3-5.3.1-Linux-x86_64.sh`<br/>
`chmod +x Anaconda3-5.3.1-Linux-x86_64.sh`<br/>
`./Anaconda3-5.3.1-Linux-x86_64.sh`<br/>

## Python PATH
1. First open profile in editor: <br/>
`vim ~/.profile` or `vim ~/.bashrc`

2. Insert Python PATH:  <br/>
`export PYTHON=/usr/bin/python<NUMER_VERSION>`

3. Update profile/bashrc: <br/>
`sudo vim ~/.bashrc`<br/>
`source ~/.bashrc` or `.  ~/.bashrc `

## Change versions of python
CMD: `update-alternatives` symbolic links determining default commands

- Check version<br/>
`python --version`

- Check where´s binary Python<br/>
`python --version`

_By default python 2.7 in /usr/bin/python<NUMER_VERSION>_

- Install multiples pythons<br/>
`update-alternatives --install /usr/bin/python python /usr/bin/python<NUMER_VERSION> 1`<br/><br/>
`update-alternatives --install /usr/bin/python python /usr/bin/python<OTHER_NUMER_VERSION> 2`<br/>

- Alter python versions<br/>
`sudo update-alternatives --config python`

 <img src="images/python_alternatives.png" width="1000" />

- Check changes<br/>
`python --version`
---

## What is Python?
É uma linguagem de programação interpretada.<br/>
Paradigmas:
- imperativa
- orientada à objetos
- funcional
- scripts

---

## Zen of Python
`import this`<br/>

---

## Keys words:
```
and        del        from        not        while
as         elif       global      or         with
assert     else       if          pass       yield
break      except     import      print
class      exec       in          raise
continue   finally    is          return
def        for        lambda      try
```

---

## Types

<img src="images/Python_3._The_standard_type_hierarchy.png" width="1000" />

---

## Interpreter and compiler

 <img src="images/cpython.png" width="299" />
 <br/>

### CPython
Compiler and interpreter bytecode, write in C.


### Jython <img src="images/jython.jpg"  width="50" />

Compiler and interpreter Java bytecode, wirte in Java.


### Comparian

<img src="images/comp-interpreter.png" />

### Why use alter compiler python?

**CPython:** torna muito fácil escrever extensões C para seu código Python porque no final ele é executado por um interpretador C. <br/>
**Jython:**, por outro lado, torna muito fácil trabalhar com outros programas Java: você pode importar qualquer classe Java sem esforço adicional, chamando e utilizando suas classes Java de dentro de seus programas Jython.

---

### How Python program run ?

<img src="images/interpreter.png" width="500" />

1. First Python checks for program syntax
2. Compiles and converts it to bytecode and directly bytecode is loaded in system memory.
3. Then compiled bytecode interpreted from memory to execute it.

---

## PEP 8
Diz sobre a qualidade de cógido (sintaxe)
https://realpython.com/python-pep8/#naming-conventions
