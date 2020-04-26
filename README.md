# PyBytom

[![Build Status](https://travis-ci.org/meherett/pybytom.svg?branch=master)](https://travis-ci.org/meherett/pybytom)
[![PyPI Version](https://img.shields.io/pypi/v/pybytom.svg?color=blue)](https://pypi.org/project/pybytom)
[![Coverage Status](https://coveralls.io/repos/github/meherett/pybytom/badge.svg?branch=master)](https://coveralls.io/github/meherett/pybytom?branch=master)

Python library with tools for Bytom blockchain.

### Installation
```
$ pip install pybytom
```

Or clone it locally, and run:

```
$ pip install -e . -r requirements.txt
```

### Quick Usage
```python
#!/usr/bin/env python3

from bytom.signature import sign, verify

# Bytom private key and public key
PRIVATE_KEY = "e07af52746e7cccd0a7d1fba6651a6f474bada481f34b1c5bab5e2d71e36ee515803ee0a6682fb19e279d8f4f7acebee8abd0fc74771c71565f9a9643fd77141"
PUBLIC_KEY = "91ff7f525ff40874c4f47f0cab42e46e3bf53adad59adef9558ad1b6448f22e2"
# Message data
MESSAGE = "1246b84985e1ab5f83f4ec2bdf271114666fd3d9e24d12981a3c861b9ed523c6"

# Signing message by private key
signature = sign(private=PRIVATE_KEY, message=MESSAGE)
print("Signature:", signature)

# Verifying signature by public key
verified = verify(public=PUBLIC_KEY, signature=signature, message=MESSAGE)
print("Verified:", verified)
```

<details open>
  <summary>Output</summary><br/>

```python
Signature: f6624fea84fadccbc1bc72dc384f662468e271c4e32d846bc0a1524470549992c8ffcc3ca43891a30de4235392b0868c506ed254f0f77cc1f2b9c1a2385ddb05
Verified: True
```
</details>

### Testing
You can run the tests with:

```
$ pytest
```

Or use `tox` to run the complete suite against the full set of build targets, or pytest to run specific 
tests against a specific version of Python.

### License
Distributed under the [MIT](https://github.com/meherett/pybytom/blob/master/LICENSE) license. See ``LICENSE`` for more information.
