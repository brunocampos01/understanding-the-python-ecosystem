# Find all files within a path

Find all files within a path, with a given file name suffix. Note that a path may contain further
subdirectories and those subdirectories may also contain furthersubdirectories. There is no limit
to the depth of the subdirectories.
Arguments:
suffix(str): suffix if the file name to be found
path(str): path of the file system
Returns:
a list of paths and file names that match the suffix

Expected deliverable
Your code should be executable with the following call “yourScript.py *.log /var/tmp”.
See below for an example of what the output should be (for a given scenario):
Scenario:
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
### Requisite

| Requisite | Version |
| --------- | ------- |
| Python    | 3.9.7   |

```bash
# application example
python first_exercise/app/find_files.py *.md /home/$USER

# tests
python -m unittest first_exercise/test/test_find_files.py
```

---
