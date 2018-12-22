# Environment Virtual Python

The Python can is executed in a environment virtual with isolation from system.<br/>
Each virtual environment has its **own Python binary**.
 <img src="images/venv.png" />

### Install
`pip install virtualenv` <br/>
or<br/>
`python3 -m venv /path/to/new/virtual/environment`

 <img src="images/env.png" />


### Create environment
`virtualenv -p python3 NAME-ENVIRONMENT`

### Init
`source <DIR>/bin/activate`

### Install libraries
`venv/bin/pip3 install NAME-LIBRARIES`

---

## Requeriments

### Visualize libraries installs
`venv/bin/pip3 freeze`

 <img src="images/freeze.png" />

- It´s passing address the *pip* the environment virtual

### Visualize libraries installs
`venv/bin/pip3 freeze > requirements.txt`

 <img src="images/requeriments.png" />


### Install libraries in requirements
`pip install -r requirements.txt`
- -r (recursive)

### References
- https://realpython.com/python-virtual-environments-a-primer/
