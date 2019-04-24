# Managemant Libraries

- pip
- poetry
- conda
- pipenv


# pip vs easy_install

# Wheel vs Egg¶


# install_requires vs requirements files¶

install_requires is a setuptools setup.py keyword that should be used to specify what a project minimally needs to run correctly.

For example, if the project requires A and B, your install_requires would be like so:

```
install_requires=[
   'A',
   'B'
]
```


For example, it may be known, that your project requires at least v1 of ‘A’, and v2 of ‘B’, so it would be like so:
```
install_requires=[
   'A>=1',
   'B>=2'
]
```

NOTE: It is not considered best practice to use install_requires to pin dependencies to specific versions

The diference beetween requires and requiremets is the user from **gaining the benefit of dependency upgrades.**

Whereas install_requires defines the dependencies for a single project, Requirements Files are often used to define the requirements for a complete Python environment.


# Requirements

### Pinned Version Numbers
Pinning the versions of your dependencies in the requirements file protects you from bugs or incompatibilities in newly released versions:
```
SomePackage == 1.2.3
DependencyOfSomePackage == 4.5.6
```

Using pip freeze to generate the requirements file will ensure that not only the top-level dependencies are included but their sub-dependencies as well, and so on. Perform the installation using –no-deps for an extra dose of insurance against installing anything not explicitly listed.


Requirements files are used to hold the result from pip freeze for the purpose of achieving repeatable installations. In this case, your requirement file contains a pinned version of everything that was installed when pip freeze was run.
```
pip freeze > requirements.txt
pip install -r requirements.txt
```

Requirements files are used to force pip to properly resolve dependencies.

### References:
- https://pip.pypa.io/en/latest/user_guide/#repeatability
