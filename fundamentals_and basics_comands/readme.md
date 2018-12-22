# Fundamentals
  - What is Python?
  - Keys words
  - Interpreter Python
  - How Python program run ?
  - Environment Virtual
  - Libraries

# PEP 8
- https://realpython.com/python-pep8/#naming-conventions

---

## What is Python?
É uma linguagem de script de programação interpretada.<br/>
Paradigmas:
- imperativa
- orientada à objetos
- funcional

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