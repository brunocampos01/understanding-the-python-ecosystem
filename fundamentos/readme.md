# Environment Virtual Python
The Python can is executed in a environment virtual **slice** without installs.

### Install
`pip install virtualenv`
env.png

### Create environment
`virtualenv -p python3 NAME-ENVIRONMENT`
- The virtualenv create repository with name NAME-ENVIRONMENT

### Init
`. venv/bin/activate`

### Install libraries
`venv/bin/pip3 install NAME-LIBRARIES

---

# Creating Requeriments

### Visualize libraries installs
`venv/bin/pip3 freeze`
freeze.png
- It´s passing address the *pip* the environment virtual

### Visualize libraries installs
`venv/bin/pip3 freeze > requirements.txt`
requirements.png

### Install libraries in requirements
`pip install -r requirements.txt`
- -r (recursive)
