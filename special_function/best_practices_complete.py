from time import sleep


print("This is my file to demonstrate best practices.\n")


def process_data(data: str) -> str:
    """
    Example Function with DocStrings and Annotation Function.
    In this file Python view the best pratices write a Python file using main()

    Args:
        big_table: A data to process.

    Returns:
        A data changed of type String.

    Raises:
        None.
    """
    print("Beginning data processing...")
    modified_data = data + " that has been modified"  # type: str
    sleep(8)
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
    # execute only if run as a script
    main()
