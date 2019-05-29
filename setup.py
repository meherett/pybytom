from setuptools import setup

with open("README.md", "r") as readme:
    long_description = readme.read()

setup(
    name="btmhdw",
    version='0.1.0',
    description='The implementation of Hierarchical Deterministic (HD) wallets generator for Bytom protocol',
    long_description=long_description,
    long_description_content_type="text/markdown",
    license='MIT',
    author='Meheret Tesfaye',
    author_email='meherett@zoho.com',
    url='https://github.com/mehetett/btmhdw',
    python_requires='>=3.5,<3.7',
    packages=['btmhdw'],
    install_requires=[
        "mnemonic==0.13",
        "two1==3.10.9"
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7"
    ],
)
