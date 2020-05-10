# pybytom

[![Build Status](https://travis-ci.org/meherett/pybytom.svg?branch=master)](https://travis-ci.org/meherett/pybytom)
[![PyPI Version](https://img.shields.io/pypi/v/pybytom.svg?color=blue)](https://pypi.org/project/pybytom)
[![Coverage Status](https://coveralls.io/repos/github/meherett/pybytom/badge.svg?branch=master)](https://coveralls.io/github/meherett/pybytom?branch=master)

Python library with tools for Bytom blockchain. [Wiki Documentation](https://github.com/meherett/pybytom/wiki)

### Installation

```
$ pip install pybytom
```

Or clone it locally, and run:

```
$ pip install -e .[tests] -r requirements.txt
```

### Quick Usage

bytom wallet

```python
#!/usr/bin/env python3

from pybytom.wallet import Wallet
from pybytom.utils import generate_entropy

import json

# 128 strength entropy
ENTROPY = generate_entropy(strength=128)
# Secret passphrase
PASSPHRASE = None  # str("meherett")
# Choose language english, french, italian, spanish, chinese_simplified, chinese_traditional, japanese & korean
LANGUAGE = "chinese_traditional"  # default is english

# Initialize wallet
wallet = Wallet()
# Get Bytom wallet from entropy
wallet.from_entropy(entropy=ENTROPY, passphrase=PASSPHRASE, language=LANGUAGE)

# Derivation from path
# wallet.from_path("m/44/153/47/61/89")
# Or derivation from index
wallet.from_index(44)
wallet.from_index(153)
wallet.from_index(47)
wallet.from_index(61)
wallet.from_index(89)
# Or derivation from indexes
# wallet.from_indexes(["2c000000", "99000000", "2f000000", "3d000000", "59000000"])

# Print all wallet information's
print(json.dumps(wallet.dumps(), indent=4, ensure_ascii=False))
```

<details>
  <summary>Output</summary><br/>

```json5
{
    "entropy": "3c091018b2ab6979f9abfe92a00db76d",
    "mnemonic": "包 輕 種 脫 漁 尋 紳 哈 贊 在 染 咬",
    "language": "chinese_traditional",
    "passphrase": null,
    "seed": "19fd77fad2e1a487c9b24402b3165edafaadcfb7355481ddb5bf7bdca9bb064370c60b47cdd105436ed096a65049f8e38350c9385b4f5126ad25932e78dd2727",
    "xprivate_key": "880e69c2343398c944609e2d741035c22c4d7d4a17074ec633445c99b31fed53b56e17e0103e0f8c8d4d5b4ba11721b901eee8f873a27ea70a59fd2f11f107cf",
    "xpublic_key": "9840c0787fa20b46ff26000e529100275ddc9facf978a57c2e0853687d18efe0b56e17e0103e0f8c8d4d5b4ba11721b901eee8f873a27ea70a59fd2f11f107cf",
    "expand_xprivate_key": "880e69c2343398c944609e2d741035c22c4d7d4a17074ec633445c99b31fed53f2aa8d931488aaecec9fa4554ee67b13aee298b12344d2541a501b37458775ad",
    "indexes": ["2c000000", "99000000", "2f000000", "3d000000", "59000000"],
    "path": "m/44/153/47/61/89",
    "child_xprivate_key": "2075790b2ad2c970926303d843973487e7dd731b0c2f5427280d04e39e24ed53cfc5ba27faa74cce710425d6542707e2ce6a43a914bd50cb9296bd236203a73e",
    "child_xpublic_key": "6788030d4c88ce2c460bc93839baa3b97ee21a6e48b0b6e4ba79de8667be6200cfc5ba27faa74cce710425d6542707e2ce6a43a914bd50cb9296bd236203a73e",
    "private_key": "2075790b2ad2c970926303d843973487e7dd731b0c2f5427280d04e39e24ed53cfc5ba27faa74cce710425d6542707e2ce6a43a914bd50cb9296bd236203a73e",
    "public_key": "6788030d4c88ce2c460bc93839baa3b97ee21a6e48b0b6e4ba79de8667be6200",
    "program": "00143ba4efd026eb3a5123964be1d68374ce15d03ecb",
    "address": {
        "mainnet": "bm1q8wjwl5pxava9zgukf0sadqm5ec2aq0kt84hpxn",
        "solonet": "sm1q8wjwl5pxava9zgukf0sadqm5ec2aq0ktxyaqxa",
        "testnet": "tm1q8wjwl5pxava9zgukf0sadqm5ec2aq0ktrrk9xz"
    }
}
```
</details>

bytom core wallet

```python
#!/usr/bin/env python3

from pybytom.wallet import Wallet
from pybytom.utils import generate_mnemonic

# Initialize wallet
wallet = Wallet(network="mainnet")  # mainnet, solonet & testnet
# Get Bytom wallet from mnemonic
wallet.from_mnemonic(mnemonic=generate_mnemonic(language="spanish"), passphrase=None)

# Set account index & addresses for change
ACCOUNT_INDEX, ADDRESSES_FOR_CHANGE = 1, True

print("Mnemonic:", wallet.mnemonic())
print("XPrivate Key:", wallet.xprivate_key())
print("XPublic Key:", wallet.xpublic_key())
print("Base HD Path:  m/44/153/{ACCOUNT_INDEX}/{ADDRESSES_FOR_CHANGE}/{ADDRESS_INDEX}")

print("\nAddresses For Change:", ADDRESSES_FOR_CHANGE)
# Get account index 1 wallet information's
for address_index in range(1, 10):
    # Derivation from path
    wallet.from_path(f"m/44/153/{ACCOUNT_INDEX}/{1 if ADDRESSES_FOR_CHANGE else 0}/{address_index}")
    # Print account_index, change, addresses_index, address and private_key like bytom core wallet accounts
    print(f"({ACCOUNT_INDEX}) ({ADDRESSES_FOR_CHANGE}) ({address_index}) {wallet.address()} {wallet.private_key()}")
    # Clean derivation
    wallet.clean_derivation()
```

<details>
  <summary>Output</summary><br/>

```shell script
Mnemonic: mil menor rayo combate poesía experto nobleza helado producto archivo nuez gota
XPrivate Key: 58c6f366f5d0bbd9d3699dc1fa7d1c5417d88001c6b37473c12152429518ed4b4f4a530aa5c277634a8cbc938ab2dc3f7a4725aebf588a0ea68b1c836c9fd7cd
XPublic Key: f91d22b752ebf12f55b55aa27da2f61f56778ce79bfc05e7c7076214284572fa4f4a530aa5c277634a8cbc938ab2dc3f7a4725aebf588a0ea68b1c836c9fd7cd
Base HD Path:  m/44/153/{ACCOUNT_INDEX}/{ADDRESSES_FOR_CHANGE}/{ADDRESS_INDEX}

Addresses For Change: True
(1) (True) (1) bm1qyaqy8el45mfs09gu8w8ll4rj7zz6s6uk4q6ztg 00e6b5c7a8e548790453a5bc2cf02e6ad1714dae101c664796484973b61ced4b874b13f7af830a372338657464d22cfa89abb7b8b985caf2e53c2874670cddb5
(1) (True) (2) bm1qx4eyc63jptx4j4vt4zre2739eqzczsq9nqc49p 306923b45a8ee4bd7733c25ecc77ac8ee02cb7dfeb77575fc1024743e91bed4b463392716d6a4edafde88873791e245a137c6cbc5bf3a45edd45343f10ee72a8
(1) (True) (3) bm1qsfcgzlquh6p0qlgcymmvg7ax4mffx9hgwpllf9 70a814f38c53aa739ead9b9def99138b7765ca79c2f374680a6e9af1d21bed4bd75cf2e6926ded7310c3f06656a95c8aa00751b942cc460904b4d94c9a1fb76a
(1) (True) (4) bm1q9nf24pfw0krhxdzh54ffynvn5qc9xjd45le7lu b8817ee3bc3e7fe5c27fd1f0e2f5bfe50a1f786ac1816f98052252032d1bed4b33ea04e95bbeb0bafb7b5be23dfa751a765554d21a437b29c6b261ae9a4cf3b3
(1) (True) (5) bm1qtwtdhf6jmxhfhutjacmgxyv6levnkuhad67wqh e81ff91277be5438c1041dbd926dac509750c2c477c479135007f7d99e1bed4ba59c4d4b0dd0d19f0c38bbd48f91309774a33f389b16932a409633d37aacf0a7
(1) (True) (6) bm1qt5l8vls6u9wwjqqnpc37c06cp9sl6ufw4dspkh 986e28479255be5e9134602cb1ee95397ea3c0c7073cc572a7671d28051ced4b143b1fb550d989ca122531d459e675f5782e24d31a0da06b14915e436712036c
(1) (True) (7) bm1qr3h0ljhcgwu0h09teegk638my30c29a3aerjg2 e887c194e28b167f487e27b34323c74fdbf1f7572657be2301176646b21bed4b9d2d7a8b35034f99486571babb2548149a6dce3c4afbfa3b6462d6bbdb1d9827
(1) (True) (8) bm1qwk4kpx09ehccrna3enqqwhrj9xt7pwxd4sufkw 48d8d9a4e612faa554259e5048d4e3f0482516542537feb3e05e9b29ce1bed4b3ab2fefbd4da07acc4ef595a119240c0fb7f95ae04f650fd21a75c7cecc1736c
(1) (True) (9) bm1qdkysl2fga28jv2u7kq9rxh4rq43ttdh4u59yld 30e7f8019becac6b6dcb59be924fd040ee5ad4e8194732e47fb3e9c4421ced4bb648c555be34b7d01e79b354c6033e755486c1f973cf802ad0f9b9ee015652b5
```
</details>

bytom signature

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

```shell script
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
