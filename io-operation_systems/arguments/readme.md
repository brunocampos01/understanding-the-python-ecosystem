# Arguments

 arguments thereafter are turned into a list of strings  and assigned to the `sys.argv` variable.


## Argparse
- Basic
```Python
import argparse


parser = argparse.ArgumentParser()
parser.parse_args()
```
- Collects the arguments and requires app to call methods
- Provides method .error for customization of error messages
- Supports only file opening


#### Examples Error Handling
argparse not run exceptions
```python
def validate(args):
    try:
        args = schema.validate(args)
        return args
    except SchemaError as e:
        exit(e)

    if arguments['<command>'] == 'hello':
        greet(validate(docopt(HELLO)))
    elif arguments['<command>'] == 'goodbye':
        greet(validate(docopt(GOODBYE)))
```


Arparse is the standard library (included with Python) for creating command-line utilities.


## `sys.argv` or `argparse`
sys.argv is simply a list of the commandline arguments.


argparse is a full featured commandline parser which generally parses sys.argv and gives you back the data in a much easier to use fashion.

## Docopt
docopt has implementations for many other languages.

## Click
 The decorator style implementation of click is very simple to use and since you are decorating the function you want executed, it makes it very easy to read the code and figure out what is going to be executed
