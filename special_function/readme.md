## Main()

Many programming languages have a special functions that is automatically executed when an operation system starts to run.

This function is often called the **entry point** because it is where execution enters the program.

The Python interpreter is not have special functions that serves as the entry point

Nevertheless (pt:mesmo assim) have convetions to define start execution.


### A Basic Python main()
```python
def main():
    print("Hello World!")
    

if __name__ == "__main__":
    # execute only if run as a script
    main()
```

###  4 Best Practices

1. Put most code into a function or class.
2. Use `__name__` to control execution of your code.
3. Create a function called main() to contain the code you want to run.
4. Call other functions from main().


##### Put most code into a function or class

Sometimes the code you write will have side effects that you want the user to control, such as:

- Running a computation that takes a long time
- Writing to a file on the disk
- Printing information that would clutter the user’s terminal

**why?**<br/>
This is because when the Python interpreter encounters the def or class keywords, it only stores those definitions for later use and doesn’t actually execute them until you tell it to.

Example: `best_pratices.py`
```python
from time import sleep

print("This is my file to demonstrate best practices.")

def process_data(data):
    print("Beginning data processing...")
    modified_data = data + " that has been modified"
    sleep(3)
    print("Data processing finished.")
    return modified_data
    
```

##### Use __name__ to Control the Execution of Your Code

```python
from time import sleep

print("This is my file to demonstrate best practices.")

def process_data(data):
    print("Beginning data processing...")
    modified_data = data + " that has been modified"
    sleep(3)
    print("Data processing finished.")
    return modified_data
    
if __name__ == "__main__":
    data = "My data read from the Web"
    print(data)
    modified_data = process_data(data)
    print(modified_data)
    
```

##### Create a Function Called main() to Contain the Code You Want to Run
Although Python does not assign any significance to a function named main(), the best practice is to name the entry point function main() anyways.


**why?**<br/>
 That way, any other programmers who read your script immediately know that this function is the starting point of the code that accomplishes the primary task of the script.
```python
from time import sleep

print("This is my file to demonstrate best practices.")

def process_data(data):
    print("Beginning data processing...")
    modified_data = data + " that has been modified"
    sleep(3)
    print("Data processing finished.")
    return modified_data

def main():
    data = "My data read from the Web"
    print(data)
    modified_data = process_data(data)
    print(modified_data)

if __name__ == "__main__":
    main()
```

##### Call Other Functions From main()

The function `main()` must execute other functions.


To reuse functionality

Examples:
```python
from time import sleep


print("This is my file to demonstrate best practices.")


def process_data(data):
    print("Beginning data processing...")
    modified_data = data + " that has been modified"
    sleep(3)
    print("Data processing finished.")
    return modified_data


def read_data_from_web():
    print("Reading data from the Web")
    data = "Data from the web"
    return data


def write_data_to_database(data):
    print("Writing data to a database")
    print(data)


def main():
    data = read_data_from_web()
    modified_data = process_data(data)
    write_data_to_database(modified_data)


if __name__ == "__main__":
    main()
```

Now, you can run the whole processing pipeline from the command line, as shown below:

```bash
$ python3 best_practices.py
This is my file to demonstrate best practices.
Reading data from the Web
Beginning data processing...
Data processing finished.
Writing processed data to a database
Data from the web that has been modified
```

## References:
- https://realpython.com/python-main-function/
- https://docs.python.org/3/library/__main__.html 
