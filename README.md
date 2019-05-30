<p align="start">		
  <img src="https://raw.githubusercontent.com/meherett/btmhdw/master/btmhdw.png">		
</p>

# btmhdw

*The implementation of Hierarchical Deterministic (HD) wallets generator for Bytom blockchain.*

![GitHub License](https://img.shields.io/github/license/cobraframework/pytest-cobra.svg)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/bip32key.svg)
![PyPI Version](https://img.shields.io/pypi/v/pytest-cobra.svg?color=red)
![PyPI Wheel](https://img.shields.io/pypi/wheel/pytest-cobra.svg?color=black)
[![Donate with Bitcoin](https://en.cryptobadges.io/badge/micro/3JiPsp6bT6PkXF3f9yZsL5hrdQwtVuXXAk)](https://en.cryptobadges.io/donate/3JiPsp6bT6PkXF3f9yZsL5hrdQwtVuXXAk)



## Installation
Install btmhdw
```
pip install btmhdw
```

## Development
Clone the repository and then run
```
pip install -e . -r requirements.txt
```

## Running the test
You can run the tests with:
```
py.test tests
```

## Usage
#### Create a new Bytom wallet
```python
from btmhdw import BTMHDW

# init BTMHDW
btmhdw = BTMHDW()

# Generate mnemonic english/japanese
mnemonic = btmhdw.generateMnemonic("english")

# Checking mnemonic language
if not btmhdw.checkMnemonic(mnemonic, "english"):
    exit()

# Create a new wallet
createdWallet = btmhdw.createWallet(mnemonic=mnemonic, network="mainnet")

print(createdWallet)
```
`OUTPUT`
```json5
  {
     entropy: "...",
     mnemonic: "...",
     address: "...",
     seed: "...",
     xprivate: "...",
     xpublic: "...",
     program: "...",
     path: "..."
  }
```

#### Get wallet from XPrivate key
```python
from btmhdw import BTMHDW

XPRIVATE = "c003f4bcccf9ad6f05ad2c84fa5ff98430eb8e73de5de232bc29334c7d074759d513bc370335cac51d77f0be5dfe84de024cfee562530b4d873b5f5e2ff4f57c"

# init BTMHDW
btmhdw = BTMHDW()

# Wallet from xprivate
walletFromXPrivate = btmhdw.walletFromXPrivate(xprivate=XPRIVATE,
                                               network="mainnet")
```
`OUTPUT`
```json5
  {
     address: "...",
     xprivate: "...",
     xpublic: "...",
     program: "...",
     path: "..."
  }
```

## Example
Here are more [btmhdw/example](https://github.com/meherett/btmhdw/example/master/example.py)

## API

#### BTMHDW()
**`generateMnemonic()`**: It is to generate new mnemonic.

**Parameters**

`Optional`:
- `String` - *strength*, 128.
- `String` - *passphrase*, password of the key.
- `String` - *language*, mnemonic language of the key.

**Returns**

`Object`:
- `String` - *mnemonic*, new mnemonic mnemonic 12 words.

**`checkMnemonic()`**: It is to check mnemonic language.

**Parameters**

`Object`:
- `String` - *mnemonic*, mnemonic 12 words.

`Optional`:
- `String` - *language*, english/japanese by default english.

**Returns**

`Object`:
- `Boolean` - *boolean*, True/False.

**`createWallet()`**: It is to create new Bytom wallet.

**Parameters**

`Optional`:
- `String` - *mnemonic*, mnemonic 12 words.
- `String` - *passphrase*, password of the key.
- `String` - *account*, account path index by default 1.
- `String` - *change*, change path index 0 or 1 by default 0.
- `String` - *address*, address path index by default 1.
- `String` - *path*, indexes string of index to create wallet address.
- `Array` - *indexes*, indexes array of index to create wallet address.
- `String` - *network*, mainnet(bm)/testnet(tm)/solonet(sm) by default sm.

**Returns**

`Object`:
- `Object` - *object*, keys are _entropy_, _mnemonic_, _address_, _seed_, _xprivate_, _xpublic_, _program_ and _path_

**`walletFromXPrivate()`**: It is to get wallet from XPrivate

**Parameters**

`Object`:
- `String` - *xprivate*, xprivate key.

`Optional`:
- `String` - *account*, account path index by default 1.
- `String` - *change*, change path index 0 or 1 by default 0.
- `String` - *address*, address path index by default 1.
- `String` - *path*, indexes string of index to create wallet address.
- `Array` - *indexes*, indexes array of index to create wallet address.
- `String` - *network*, mainnet(bm)/testnet(tm)/solonet(sm) by default sm.

**Returns**

`Object`:
- `Object` - *object*, keys are entropy, mnemonic, address, seed, xprivate, xpublic, program and path

#### BytomHDWallet()

**`masterKeyFromMnemonic()`**: It is to get master key from mnemonic.

**Parameters**

`Object`:
- `String` - *mnemonic*, mnemonic 12 words.

`Optional`:
- `String` - *passphrase*, password of the key.

**Returns**

`Object`:
- `Object` - *BytomHDWallet()*, BytomHDWallet class.

**`generateEntropy()`**: It is to generate new entropy.

**Returns**

`Object`:
- `String` - *entropy*, entropy hex.

**`masterKeyFromEntropy()`**: It is to get master key from mnemonic.

**Parameters**

`Optional`:
- `String` - *entropy*, new entropy.
- `String` - *strength*, 128.
- `String` - *passphrase*, password of the key.
- `String` - *language*, mnemonic language of the key.

**Returns**

`Object`:
- `Object` - *BytomHDWallet()*, BytomHDWallet class.
- `String` - *mnemonic*, mnemonic 12 words.

**`masterKeyFromXPrivate()`**: It is to get master key from XPrivate.

**Parameters**

`Object`:
- `String` - *xprivate*, BTM xprivate key.

**Returns**

`Object`:
- `Object` - *BytomHDWallet()*, BytomHDWallet class.

**`xprivateKey()`**: It is to get XPrivate key.

**Returns**

`Object`:
- `String` - *xprivate*, btm wallet xprivate key.

**`xpublicKey()`**: It is to get XPublic key.

**Parameters**

`Optional`:
- `String` - *xprivate*, BTM xprivate key.

**Returns**

`Object`:
- `String` - *xpublic*, btm wallet xpublic key.

**`expandPrivateKey()`**: It is to get Expand XPrivate key.

**Parameters**

`Optional`:
- `String` - *xprivate*, BTM xprivate key.

**Returns**

`Object`:
- `String` - *expandPrivate*, btm wallet expand private key.

**`publicKey()`**: It is to get public key(length 64).

**Parameters**

`Optional`:
- `String` - *xpublic*, BTM xpublic key.

**Returns**

`Object`:
- `String` - *public*, btm wallet public key(length 64).

**`fromIndexes()`**: It is to set collection of index.

**Parameters**

`Object`:
- `Array` - *indexes*, array of index.

**`fromIndex()`**: It is to set index.

**Parameters**

`Object`:
- `Number` - *index*, number.

**Returns**

`Object`:
- `Object` - *BytomHDWallet()*, BytomHDWallet class.

**`fromPath()`**: It is to set index from path.

**Parameters**

`Object`:
- `String` - *path*, path of index.

**Returns**

`Object`:
- `Object` - *BytomHDWallet()*, BytomHDWallet class.

**`getIndexes()`**: It is to get collection of index.

**Returns**

`Object`:
- `Array` - *indexes*, collection of index.

**`getPath()`**: It is to get path of indexes.

**Returns**

`Object`:
- `String` - *path*, path indexes.









## Author ✒️

* ***Meheret Tesfaye*** - *Initial work* - [Cobra](https://github.com/cobraframework)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details
