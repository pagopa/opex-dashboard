#!/usr/bin/env python

from os.path import dirname, join
from setuptools import find_packages, setup
from src import opex_dashboard

def read(fname):
    return open(join(dirname(__file__), fname)).read()

setup(
    name=opex_dashboard.__title__,
    author=opex_dashboard.__author__,
    url="https://github.com/pagopa/operational-excellence-dashboard",
    project_urls={
        "Source": "https://github.com/pagopa/operational-excellence-dashboard",
    },
    version=opex_dashboard.__version__,
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    description=opex_dashboard.__description__,
    long_description=read("README.md"),
    long_description_content_type="text/markdown",
    keywords="openapi3, swagger, python",
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.9",
        "Topic :: Software Development :: Libraries",
    ],
    install_requires=[
        # "prance>=0.20.2",
        # "openapi-spec-validator>=0.2.9",
    ],
)
