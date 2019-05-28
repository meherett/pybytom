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
    url='https://github.com/mehetett/bytom-hdwallet',
    python_requires='>=3.5,<3.7',
    packages=['btmhdw'],
    install_requires=[
        "ed25519>=1.4",
        "pbkdf2>=1.3",
        "pybase64>=0.5.0",
        "qrcode>=6.1",
        "sha3>=0.2.1",
        "six>=1.12.0"
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7"
    ],
)
