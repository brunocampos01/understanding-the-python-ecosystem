import sys
import os

if len(sys.argv) > 1:
    print("Hello from child process", os.getpid(), sys.argv[1])
else:
    print("Hello from child process", os.getpid(), "(no argument)")
