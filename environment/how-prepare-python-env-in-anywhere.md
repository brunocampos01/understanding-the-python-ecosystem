# Running

1. [Local](#running-in-local)
2. [Development: Virtual Environment](#running-in-virtual-environment)
3. [Deploy: Container](#running-in-container)


## Running in Local

- Install Python Dependencies, Test python environment and Delete all compiled Python files.

```shell script
sudo make

# Available rules:

# clean                       Delete all compiled Python files
# lint                        Lint using flake8
# install_requirements        Install Python Dependencies
# test_environment            Test python environment is setup correctly
```

```shell script
make install_requirements
make test_environment
make clean
```

---

## Running in Virtual Environment

- Create virtual environment

```shell script
virtualenv -p python3 venv
```

- Activate this semi-isolated environment

```shell script
source venv/bin/activate
```

- Install the libraries

```shell script
pip3 install -r requirements.txt
```

---

## Running in Container

- It's necessary be in home this project

```sh
name_project=$(basename "$(pwd)")
echo $name_project
sudo docker build --no-cache -t $name_project -f src/environment/container/Dockerfile .
sudo docker run -it -p 8888:8888 $name_project
```
