from __future__ import print_function
from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand
import io
import codecs
import os
import sys

import luigi_warehouse

here = os.path.abspath(os.path.dirname(__file__))


def read(*filenames, **kwargs):
    encoding = kwargs.get('encoding', 'utf-8')
    sep = kwargs.get('sep', '\n')
    buf = []
    for filename in filenames:
        with io.open(filename, encoding=encoding) as f:
            buf.append(f.read())
    return sep.join(buf)


long_description = '''
                      Luigi-Warehouse
                      ===============

                      A boilerplate implementation of `Luigi`_ at Groupon
                      ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

                      .. figure:: https://i.kinja-img.com/gawker-media/image/upload/s--u1D3aUdn--/p5onht9mlgdkj0yvnjao.jpg
                         :alt: pic

                         pic

                      -  `Luigi`_ is a Python package that helps you build complex pipelines
                         of batch jobs. It handles dependency resolution, workflow management,
                         visualization, handling failures, command line integration, and much
                         more

                      -  Luigi-Warehouse adds
                      -  example workflows (i.e. replicating postgresql tables to redshift)
                      -  more data sources
                      -  variable data sources that do not rely on default luigi
                         behavior/configs (i.e. ``VariableS3Client``)

                      Getting Started
                      ---------------

                      -  Some example workflows are included. Assumptions, Args & Comments are
                         in the File

                      +-------------+-----------------------------------------+-----------------------+
                      | File        | Description                             | Main Class(es)        |
                      +=============+=========================================+=======================+
                      | gsheet\_to\ | replicates all data from a google sheet | Run                   |
                      | _redshift.p | to a redshift table (full copy/replace) |                       |
                      | y           |                                         |                       |
                      +-------------+-----------------------------------------+-----------------------+
                      | postgres\_t | replicates postgres tables to redshift  | Run -                 |
                      | o\_redshift | (incrementally or full copy/replace)    | PerformIncrementalImp |
                      | .py         |                                         | ort                   |
                      |             |                                         | PerformFullImport     |
                      +-------------+-----------------------------------------+-----------------------+
                      | salesforce\ | replicates a salesforce report or SOQL  | SOQLtoRedshift        |
                      | _to\_redshi | to a redshift table(full copy/replace)  | ReporttoRedshift      |
                      | ft.py       |                                         |                       |
                      +-------------+-----------------------------------------+-----------------------+
                      | teradata\_t | replicates given teradata SQL to        | Run                   |
                      | o\_redshift | redshift table (incrementally or full   |                       |
                      | .py         | copy/replace)                           |                       |
                      +-------------+-----------------------------------------+-----------------------+
                      | typeform\_t | replicates all data from typeform       | Run                   |
                      | o\_redshift | responses to a redshift table (full     |                       |
                      | .py         | copy/replace)                           |                       |
                      +-------------+-----------------------------------------+-----------------------+
                      | zendesk\_to | extracts                                | Run                   |
                      | \_redshift. | users,orgs,tickets,ticket\_events from  |                       |
                      | py          | zendesk to redshift (partially          |                       |
                      |             | incremental)                            |                       |
                      +-------------+-----------------------------------------+-----------------------+

                      -  Example to run a workflow

                         ::

                             $ LUIGI_CONFIG_PATH=luigi.cfg && python3 modules/postgres_to_redshift.py Run --workers 50

                      .. _Luigi: http://luigi.readthedocs.org/en/stable/index.html
                      '''


class PyTest(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import pytest
        errcode = pytest.main(self.test_args)
        sys.exit(errcode)


setup(
    name='luigi_warehouse',
    version=luigi_warehouse.__version__,
    url='http://github.com/groupon/luigi-warehouse',
    license='MIT',
    author='Various',
    tests_require=['pytest'],
    # minimal install
    install_requires=['luigi>=2.0.0',
                      'boto>=2.38.0',
                      'pandas>=0.17.1',
                      'numpy'],
    cmdclass={'test': PyTest},
    description='Luigi Workflows for Replicating Data to Redshift',
    long_description=long_description,
    packages=['luigi_warehouse'],
    include_package_data=True,
    platforms='any',
    test_suite='luigi_warehouse.test.test_luigi_warehouse',
    classifiers=[
        'Programming Language :: Python',
        'Development Status :: 4 - Beta',
        'Natural Language :: English',
        'Environment :: Web Environment',
        'Intended Audience :: Developers, Data Engineers, Data Scientists',
        'License :: MIT',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    extras_require={
        'testing': ['pytest'],
    }
)
