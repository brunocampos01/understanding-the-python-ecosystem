# Publish an Open-Source Python Package to PyPI

```bash
# Publishing to PyPI
pip install twine

# Building package
python setup.py sdist bdist_wheel

# Test
twine check dist/*

# Uploading package
twine upload dist/*
```

#### Reference
- https://realpython.com/pypi-publish-python-package/