#!/usr/bin/env python
from setuptools import setup, find_packages
from os import path

here = path.abspath(path.dirname(__file__))

setup(
    name='wcst_engine',
    version='0.0.0',
    description='An engine for the WCST to train and evaluate artificial agents on',
    author='Patrick Zhang',
    author_email='pqz317@uw.edu',
    packages=find_packages(exclude=[]),
)