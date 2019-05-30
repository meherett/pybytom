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

##### Example

```python
print(btmhdw.generateMnemonic(language="english", passphrase="meherett"))
print(btmhdw.generateMnemonic(language="japanese", passphrase="meherett"))
```
<details>
<summary>Output</summary>

```python
"spare uniform possible grief attitude machine peace update tornado area evolve spread"
"あけがたãひていãぎじかがくãくうきãどうぐãだじゃれãおおうãりねんãこんだてãてわたしãはぶらしãちいき"
```
</details>

----

**`checkMnemonic()`**: It is to check mnemonic language.

**Parameters**

`Object`:
- `String` - *mnemonic*, mnemonic 12 words.

`Optional`:
- `String` - *language*, english/japanese by default english.

**Returns**

`Object`:
- `Boolean` - *boolean*, True/False.

##### Example

```python
MNEMONIC = "ancient young hurt bone shuffle deposit congress normal crack six boost despair"

print(btmhdw.checkMnemonic(MNEMONIC, "english"))
print(btmhdw.checkMnemonic(MNEMONIC, "japanese"))
```
<details>
<summary>Output</summary>

```python
True
False
```
</details>

----

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

##### Example

```python
mnemonic = btmhdw.generateMnemonic("english")
createdWallet = btmhdw.createWallet(mnemonic=mnemonic, 
                                    network="mainnet")

print(createdWallet['address'])
print(createdWallet['xprivate'], '\n')
print(createdWallet)
```
<details>
<summary>Output</summary>

```json5
"bm1q6quqkfry04q2vt52qgccrrv03e7y0atassqwy8"
"b07512cd57be8e53ae5e564282b6c080ca32388a0d6f891f47397b8e795afc5f9e16030b0999058b562cf5727e29f7eb4ca04691a4d64d2167f16ed3eb82f5a7"

{'mnemonic': 'model file denial frost story acquire guard quote pill game asthma level', 'address': 'bm1q8jgkl7ajj87qtyeav2uerjkzl0nfyqxqrjf7nw', 'seed': '50dcaed855bad335400dd9b133403c2994a4e3f9e10100862dd8201dee0e67865fe0d5e27c1dc90cc37c5b8eb57f40cbe5f9abafa290c014625b6786b49f6142', 'xprivate': 'f8724b6d3aa39c5647505821dcd31ef7f11c93e376462430af5a2985b8047048b73ab254dd6bd81bf86f086d20f3a231be779f27d544206bc0fafff36492d810', 'xpublic': '12469fbd095ea79e9e08ffa4c2059f9567316e4ec1790621f83f4c78488a0d90b73ab254dd6bd81bf86f086d20f3a231be779f27d544206bc0fafff36492d810', 'program': '0014bdf741d1fe8225c67faa7247f6915c0d776100df', 'path': 'm/44/153/1/0/1'}

```
</details>

----

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

----

#### BytomHDWallet()

**`masterKeyFromMnemonic()`**: It is to get master key from mnemonic.

**Parameters**

`Object`:
- `String` - *mnemonic*, mnemonic 12 words.

`Optional`:
- `String` - *passphrase*, password of the key.

**Returns**

`Object`:
- `Object` - *BytomHDWallet()*, class.

----

**`generateEntropy()`**: It is to generate new entropy.

**Returns**

`Object`:
- `String` - *entropy*, entropy hex.

----

**`masterKeyFromEntropy()`**: It is to get master key from mnemonic.

**Parameters**

`Optional`:
- `String` - *entropy*, new entropy.
- `String` - *strength*, 128.
- `String` - *passphrase*, password of the key.
- `String` - *language*, mnemonic language of the key.

**Returns**

`Object`:
- `Object` - *BytomHDWallet()*, class.
- `String` - *mnemonic*, mnemonic 12 words.

----

**`masterKeyFromXPrivate()`**: It is to get master key from XPrivate.

**Parameters**

`Object`:
- `String` - *xprivate*, BTM xprivate key.

**Returns**

`Object`:
- `Object` - *BytomHDWallet()*, BytomHDWallet class.

----

**`xprivateKey()`**: It is to get XPrivate key.

**Returns**

`Object`:
- `String` - *xprivate*, btm wallet xprivate key.

----

**`xpublicKey()`**: It is to get XPublic key.

**Parameters**

`Optional`:
- `String` - *xprivate*, BTM xprivate key.

**Returns**

`Object`:
- `String` - *xpublic*, btm wallet xpublic key.

----

**`expandPrivateKey()`**: It is to get Expand XPrivate key.

**Parameters**

`Optional`:
- `String` - *xprivate*, BTM xprivate key.

**Returns**

`Object`:
- `String` - *expandPrivate*, btm wallet expand private key.

----

**`publicKey()`**: It is to get public key(length 64).

**Parameters**

`Optional`:
- `String` - *xpublic*, BTM xpublic key.

**Returns**

`Object`:
- `String` - *public*, btm wallet public key(length 64).

----

**`fromIndexes()`**: It is to set collection of index.

**Parameters**

`Object`:
- `Array` - *indexes*, array of index.

----

**`fromIndex()`**: It is to set index.

**Parameters**

`Object`:
- `Number` - *index*, number.

**Returns**

`Object`:
- `Object` - *BytomHDWallet()*, class.

----

**`fromPath()`**: It is to set index from path.

**Parameters**

`Object`:
- `String` - *path*, path of index.

**Returns**

`Object`:
- `Object` - *BytomHDWallet()*, class.

----

**`getIndexes()`**: It is to get collection of index.

**Returns**

`Object`:
- `Array` - *indexes*, collection of index.

----

**`getPath()`**: It is to get path of indexes.

**Returns**

`Object`:
- `String` - *path*, path indexes.

----

**`childXPrivateKey()`**: It is to get child of XPrivate key.

**Parameters**

`Optional`:
- `String` - *xprivate*, BTM xprivate key.
- `String` - *indexes*, collection of index.

**Returns**

`Object`:
- `String` - *childXPrivate*, btm child xprivate key.

----

**`childXPublicKey()`**: It is to get child of XPublic key.

**Parameters**

`Optional`:
- `String` - *xpublic*, BTM xpublic key.
- `String` - *indexes*, collection of index.

**Returns**

`Object`:
- `String` - *childXPublic*, btm child xpublic key.

----

**`program()`**: It is to get control program.

**Parameters**

`Optional`:
- `String` - *xpublic*, BTM xpublic key.
- `String` - *path*, path of index.
- `String` - *indexes*, collection of index.

**Returns**

`Object`:
- `String` - *program*, control program.

----

**`address()`**: It is to get address.

**Parameters**

`Optional`:
- `String` - *program*, control program.
- `String` - *network*, mainnet(bm)/testnet(tm)/solonet(sm) by default sm.

**Returns**

`Object`:
- `String` - *address*, address from control program.


## Author ✒️

* ***Meheret Tesfaye*** - *Initial work* - [Cobra](https://github.com/cobraframework)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details
