#!/usr/bin/env python

import toml

from typing import List
from os.path import dirname, join
from setuptools import find_packages, setup
from src import opex_dashboard

def read(fname: str) -> str:
    return open(join(dirname(__file__), fname)).read()

def parse_deps() -> List[str]:
    packages = toml.load("Pipfile")["packages"]
    return [f"{package}{packages[package]}" for package in packages]

setup(
    name=opex_dashboard.__name__,
    author=opex_dashboard.__author__,
    url="https://github.com/pagopa/operational-excellence-dashboard",
    project_urls={
        "Source": "https://github.com/pagopa/operational-excellence-dashboard",
    },
    version=opex_dashboard.__version__,
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    package_data={"opex_dashboard.templates": ["*"]},
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
    install_requires=parse_deps(),
    entry_points={
        "console_scripts": [
            "opex_dashboard=opex_dashboard.cli:cli"
        ]
    },
)
