# pybytom

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

> #### pybytom.wallet

```python
#!/usr/bin/env python3

from pybytom.wallet import Wallet
from pybytom.utils import generate_entropy

import json

# 128 strength entropy
ENTROPY = generate_entropy(strength=128)
# Secret passphrase
PASSPHRASE = None  # str("meherett")
# Choose language english, french, italian, spanish, chinese_simplified, chinese_traditional & korean
LANGUAGE = "chinese_traditional"  # default is english

# Initialize wallet
wallet = Wallet()
# Get Bytom wallet from entropy
wallet.from_entropy(entropy=ENTROPY, passphrase=PASSPHRASE, language=LANGUAGE)

# Derivation from path
# wallet.from_path("m/44/153/1/0/1")
# Derivation from index
wallet.from_index(44)
wallet.from_index(153)
wallet.from_index(1)  # Account
wallet.from_index(0)  # Change False(0) and True(1)
wallet.from_index(1)  # Address

# Print all wallet information's
print(json.dumps(wallet.dumps(), indent=4, ensure_ascii=False))
```

<details>
  <summary>Output</summary><br/>

```json5
{
    "entropy": "e9417c55bc2a2f7f849badd6ae318fc4",
    "mnemonic": "舒 使 系 款 株 擾 麼 鄉 狗 振 誤 謀",
    "language": "chinese_traditional",
    "passphrase": null,
    "seed": "f047a0525f44bef61b8c57e47783f868c0eae8e092a3b8bf398252f39976a43cd32640b955b9cc18adfe182f74fa2d3fe0618b3ddb8377cb1c643a43adb54e07",
    "xprivate_key": "08eb01b7b3f5b242897ae34e95b1e58074b563ad0d798c7de13382e8c4e1444963b9028e938989f01da2767f2242861011b6f14173bb9bcf3255868845e06262",
    "xpublic_key": "6a5bce17073512f3d191883f0caaf7e85c3077839736f485d31c3a09a409331563b9028e938989f01da2767f2242861011b6f14173bb9bcf3255868845e06262",
    "expand_xprivate_key": "08eb01b7b3f5b242897ae34e95b1e58074b563ad0d798c7de13382e8c4e1444907e9d742893b75339e982c40e5347dc209a14a2723943dc5eb53ece0c18a0eee",
    "indexes": ["2c000000", "99000000", "01000000", "00000000", "01000000"],
    "path": "m/44/153/1/0/1",
    "child_xprivate_key": "f8ad8bcf4a97fd0503d011fba2ef9e86303426d0e4ae4e8c2dad9f4e2ae74449405d64aa3c98f599bb89d596fce3cc2238776e88f19a891f854ecc8e71f79b39",
    "child_xpublic_key": "3872846b1343786e42dc6cd999a2d84641bf1ceb481e7c42c59adc2dbb8893f6405d64aa3c98f599bb89d596fce3cc2238776e88f19a891f854ecc8e71f79b39",
    "private_key": "f8ad8bcf4a97fd0503d011fba2ef9e86303426d0e4ae4e8c2dad9f4e2ae74449405d64aa3c98f599bb89d596fce3cc2238776e88f19a891f854ecc8e71f79b39",
    "public_key": "3872846b1343786e42dc6cd999a2d84641bf1ceb481e7c42c59adc2dbb8893f6",
    "program": "0014237c463eed4e88529e31386b17ff099d9276e9e6",
    "address": {
        "mainnet": "bm1qyd7yv0hdf6y998338p430lcfnkf8d60xrwup3p",
        "solonet": "sm1qyd7yv0hdf6y998338p430lcfnkf8d60xzlkq30",
        "testnet": "tm1qyd7yv0hdf6y998338p430lcfnkf8d60x8ca93s"
    }
}
```
</details>

> #### pybytom.signature

```python
#!/usr/bin/env python3

from pybytom.signature import sign, verify

# Bytom private key and public key
PRIVATE_KEY = "e07af52746e7cccd0a7d1fba6651a6f474bada481f34b1c5bab5e2d71e36ee515803ee0a6682fb19e279d8f4f7acebee8abd0fc74771c71565f9a9643fd77141"
PUBLIC_KEY = "91ff7f525ff40874c4f47f0cab42e46e3bf53adad59adef9558ad1b6448f22e2"
# Message data
MESSAGE = "1246b84985e1ab5f83f4ec2bdf271114666fd3d9e24d12981a3c861b9ed523c6"

# Sign message by private key
signature = sign(private_key=PRIVATE_KEY, message=MESSAGE)
print("Signature:", signature)

# Verify signature by public key
verified = verify(public_key=PUBLIC_KEY, signature=signature, message=MESSAGE)
print("Verified:", verified)
```

<details>
  <summary>Output</summary><br/>

```python
Signature: f6624fea84fadccbc1bc72dc384f662468e271c4e32d846bc0a1524470549992c8ffcc3ca43891a30de4235392b0868c506ed254f0f77cc1f2b9c1a2385ddb05
Verified: True
```
</details>

[Click this to see more examples](https://github.com/meherett/pybytom/blob/master/examples).

### Testing
You can run the tests with:

```
$ pytest
```

Or use `tox` to run the complete suite against the full set of build targets, or pytest to run specific 
tests against a specific version of Python.

### License
Distributed under the [MIT](https://github.com/meherett/pybytom/blob/master/LICENSE) license. See ``LICENSE`` for more information.
