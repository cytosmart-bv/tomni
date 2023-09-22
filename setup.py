#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import find_packages, setup

with open("README.md") as readme_file:
    readme = readme_file.read()

with open("HISTORY.rst") as history_file:
    history = history_file.read()

with open("LICENSE") as license_file:
    license = license_file.read()

with open("requirements.txt") as requirements_file:
    requirements = requirements_file.read().split("\n")

setup_requirements = ["pytest-runner"]

test_requirements = ["pytest"]

setup(
    author="Tom Nijhof",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    description="Tomni is a collection of image analysis functions usefull for CytoSmart solution.",
    install_requires=requirements,
    long_description=readme + "\n\n" + history + "\n\n" + license,
    license="ACADEMIC PUBLIC LICENSE",
    long_description_content_type="text/markdown",
    include_package_data=True,
    keywords="tomni",
    name="tomni",
    packages=find_packages(include=["tomni*"], exclude=["docs*"]),
    setup_requires=setup_requirements,
    test_suite="tests",
    tests_require=test_requirements,
    url="https://github.com/cytosmart-bv/tomni",
    version="2.0.0",
    zip_safe=False,
)
