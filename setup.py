#!/usr/bin/python3

import os
from setuptools import setup

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "python-rpm_parser",
    version = "1.0",
    author = "Josip Domsic",
    author_email = "josip.domsic+github@gmail.com",
    description = ("Pure python implementation of RPM parser"),
    license = "MIT",
    keywords = "python RPM parser tool",
    url = "https://github.com/ulicar/rpm-parser/blob/master/rpm-parser",
    packages=['rpm_parser'],
    long_description=read('README.txt'),
    data_files = [
        ('/usr/local/bin/', [
            'rpmtool'
        ])
    ],
    classifiers=[
        "Development Status :: 3",
        "Topic :: Utilities",
    ],
)
