---
title: Stack (pilha)
subtitle: Understand how the stack data structure works
authors:
- admin
tags: [data_structure, big_data, stack, algorithms]
categories: []
date: "2020-06-13T00:00:00Z"
lastMod: "2020-06-13T00:00:00Z"
featured: false
draft: false

# Featured image
# To use, add an image named `featured.jpg/png` to your page's folder. 
image:
  caption: ""
  focal_point: ""

# Projects (optional).
#   Associate this post with one or more of your projects.
#   Simply enter your project's folder or file name without extension.
#   E.g. `projects = ["internal-project"]` references 
#   `content/project/deep-learning/index.md`.
#   Otherwise, set `projects = []`.
projects: []
---
# Stack

<img src="../../img/stack.gif" align="right" width="60%" weight="100%"/>

- Insert = **push**
- Remove = **pop**
- Element on top = **peek**

## How a Stack Works

- **FILO - First In Last Out**: In a stack, the first element to be inserted is the last to be removed.
- A new element is always inserted at the top of the stack.
- An element is always removed from the top of the stack.

<img src="../../img/stack.png" align="center" width="70%" weight="300" />



### Stack Applications

The most common uses of a stack are:

- **Validate parenthesis**: implementation [here](validate_parenthesis.py)
- **Check if numeric list is sorted**: implementation [here](is_sorted.py)
- **To reverse a word**: Put all the letters in a stack and pop them out. Because of the LIFO order of stack, you will get the letters in reverse order.
- **In compilers**: Compilers use the stack to calculate the value of expressions like `2 + 4 / 5 * (7 - 9)` by converting the expression to prefix or postfix form.
- **In browsers**: The back button in a browser saves all the URLs you have visited previously in a stack.

---

### Implementation


```python
import stack
import inspect


source = inspect.getsource(stack)
print(source)
```

    class Stack(object):
    
        def __init__(self):
            """Constructor"""
            self.stack = []
            self.count = 0
    
        def push(self, element):
            """Insert on top stack"""
            self.stack.append(element)
            self.count += 1
    
        def pop(self):
            """Remove on top stack"""
            if not self.is_empty():
                self.stack.pop(self.count - 1)
                self.count -= 1
    
        def remove_all_elements(self):
            """Remove all"""
            self.stack = []
    
        def get_top(self):
            """Get the last"""
            if not self.is_empty():
                return self.stack[-1]
    
            return None
    
        def is_empty(self):
            """Check if the stack is empty"""
            if self.count == 0:
                return True
    
            return False
    
        def get_length(self):
            """Return the size"""
            return self.count
    
        def show_stack(self):
            """Show each element on stack"""
            if not self.is_empty():
                print('sssssssssss')
                for e in reversed(self.stack):
                    print(e)
            else:
                print('Stack is empty')
    


### Tests


```python
stack_obj = stack.Stack()
print(stack_obj)

# add
stack_obj.push(1)
stack_obj.push(2)
stack_obj.push('Flamengo')
```

    <stack.Stack object at 0x7f07404fadc0>



```python
# show all elements
stack_obj.show_stack()
```

    sssssssssss
    Flamengo
    2
    1



```python
# get the last element
print(stack_obj.get_top())

# check if is empty
print(stack_obj.is_empty())

# Return the size
print(stack_obj.get_length())
```

    Flamengo
    False
    3



```python
# clear last stack
stack_obj.pop()

stack_obj.show_stack()
```

    sssssssssss
    2
    1



```python
# clear all
stack_obj.remove_all_elements()

stack_obj.show_stack()
```

    sssssssssss


---

Prepare file to blog


```python
# convert ipynb to markdown

!jupyter nbconvert stack.ipynb --to markdown
```

    [NbConvertApp] Converting notebook stack.ipynb to markdown
    [NbConvertApp] Writing 4147 bytes to stack.md


---
