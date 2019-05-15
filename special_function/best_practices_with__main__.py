from time import sleep


print("\nThis is my file to demonstrate best practices.")


def process_data(data):
    print("Beginning data processing...")
    modified_data = data + " that has been modified"
    sleep(3)
    print("Data processing finished.")
    return modified_data


if __name__ == "__main__":
    # execute only if run as a script
    data = "My data read from the Web"
    print(data)
    modified_data = process_data(data)
    print(modified_data)
