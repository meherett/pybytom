#!/usr/bin/env python3

from setuptools import setup, find_packages


# README.md
with open("README.md", "r", encoding="utf-8") as readme:
    long_description = readme.read()

# requirements.txt
with open("requirements.txt", "r") as _requirements:
    requirements = list(map(str.strip, _requirements.read().split("\n")))

setup(
    name="pybytom",
    version="1.1.0",
    description="Python library with tools for Bytom blockchain.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="MIT",
    author="Meheret Tesfaye",
    author_email="meherett@zoho.com",
    url="https://github.com/meherett/pybytom",
    packages=find_packages(),
    python_requires=">=3.6,<4",
    install_requires=requirements,
    extras_require={
        "tests": [
            "pytest>=5.4.1,<6",
            "pytest-cov>=2.8.1,<3"
        ]
    },
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Topic :: Software Development :: Libraries :: Python Modules"
    ],
)
