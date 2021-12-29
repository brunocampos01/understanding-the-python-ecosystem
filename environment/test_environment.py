import sys

# This project need python 3
REQUIRED_PYTHON = "python3"


def check_python_version(python_req: str):
    # major = 3
    system_major = sys.version_info.major

    if python_req == "python":
        required_major = 2
    elif python_req == "python3":
        required_major = 3
    else:
        raise ValueError("Unrecognized python interpreter: {}"
                         .format(python_req))

    if system_major != required_major:
        raise TypeError("This project requires Python {}. Found: Python {}"
                        .format(required_major, sys.version))
    else:
        print("Python Version: {}".format(sys.version))  # e.g 3.7.3
        print(">>> Development environment passes all tests!")


def main():
    check_python_version(python_req = REQUIRED_PYTHON)


if __name__ == "__main__":
    main()
