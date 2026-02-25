# Find all files within a path

Find all files within a path that match a given file name suffix. Note that a path may contain
subdirectories, and those subdirectories may also contain further subdirectories. There is no limit
to the depth of the subdirectories.

**Arguments:**
- `suffix` (str): the suffix of the file name to find
- `path` (str): the path of the file system to search

**Returns:**
A list of paths and file names that match the suffix.

**Expected deliverable:**
Your code should be executable with the following call: `yourScript.py *.log /var/tmp`.
See below for an example of what the output should be (for a given scenario):

**Scenario:**
```commandline
|-- a
| |-- bbb
| |-- bbb.log
| |-- ddd
|-- aaa.log
|-- abc.txt
```

Output:
```
./aaa.log
./a/bbb.log
```

## How to Run
### Prerequisites

| Prerequisite | Version |
| ------------ | ------- |
| Python       | 3.9+    |

```bash
# application example
python exercises/find_path/app/find_files.py "*.md" /home/$USER

# tests
python -m unittest exercises/find_path/test/test_find_files.py
```

---
