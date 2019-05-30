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

```json5
spare uniform possible grief attitude machine peace update tornado area evolve spread
あけがたãひていãぎじかがくãくうきãどうぐãだじゃれãおおうãりねんãこんだてãてわたしãはぶらしãちいき
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
bm1qsv6u5z2uxtefnehkyuetyx4llu27umqscu8vtk
983fc70dc7c4a26ff9af39af4c0cc3057565b8f70a31158a6f37e1804ae6414ea6cade89861c53fafa461e5f0e116f47a816b11ba05585b79c577531c6000ffe 

{'mnemonic': 'alarm fix day evoke void hawk pistol pulp impact farm average mask', 'address': 'bm1qsv6u5z2uxtefnehkyuetyx4llu27umqscu8vtk', 'seed': '6e269a33fb2c65b9a1966bc9579628869630d7d647792eaa3692fdae1db1a719ff4dfef17acf6027fb20ba7ce04e4715460ea2d280f69f646df1f2a6ef6ffea1', 'xprivate': '983fc70dc7c4a26ff9af39af4c0cc3057565b8f70a31158a6f37e1804ae6414ea6cade89861c53fafa461e5f0e116f47a816b11ba05585b79c577531c6000ffe', 'xpublic': '4a7bfcbccbe97aa3f92795c761697f98b6b2350597ab73c85109b025301db1aaa6cade89861c53fafa461e5f0e116f47a816b11ba05585b79c577531c6000ffe', 'program': '0014312b5e9ee3625a50847ffd5244dbc0d8f01b8566', 'path': 'm/44/153/1/0/1'}
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

##### Example

```python
XPRIVATE = "c003f4bcccf9ad6f05ad2c84fa5ff98430eb8e73de5de232bc29334c7d074759d513bc370335cac51d77f0be5dfe84de024cfee562530b4d873b5f5e2ff4f57c"
walletFromXPrivate = btmhdw.walletFromXPrivate(xprivate=XPRIVATE,
                                               network="mainnet")
print(walletFromXPrivate['address'])
print(walletFromXPrivate['xprivate'], '\n')
print(walletFromXPrivate)
```
<details>
<summary>Output</summary>

```json5
bm1qtzg058tt5eyf2qqfy2650erxqxhfkt4p236708
c003f4bcccf9ad6f05ad2c84fa5ff98430eb8e73de5de232bc29334c7d074759d513bc370335cac51d77f0be5dfe84de024cfee562530b4d873b5f5e2ff4f57c 

{'address': 'bm1qtzg058tt5eyf2qqfy2650erxqxhfkt4p236708', 'xprivate': 'c003f4bcccf9ad6f05ad2c84fa5ff98430eb8e73de5de232bc29334c7d074759d513bc370335cac51d77f0be5dfe84de024cfee562530b4d873b5f5e2ff4f57c', 'xpublic': '1b0541a7664cee929edb54d9ef21996b90546918a920a77e1cd6015d97c56563d513bc370335cac51d77f0be5dfe84de024cfee562530b4d873b5f5e2ff4f57c', 'program': '0014dcf6b21d83c978d3125d1330c928c38fee315200', 'path': 'm/44/153/1/0/1'}
```
</details>

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

##### Example

```python
MNEMONIC = "ancient young hurt bone shuffle deposit congress normal crack six boost despair"

bytomHDWallet = BytomHDWallet.masterKeyFromMnemonic(mnemonic=MNEMONIC,
                                                    passphrase="Meheret Tesfaye")
```

----

**`generateEntropy()`**: It is to generate new entropy.

**Returns**

`Object`:
- `String` - *entropy*, entropy hex.

##### Example

```python
print(bytomHDWallet.generateEntropy().hex())
```
<details>
<summary>Output</summary>

```json
7184af4506fb1b51c52d2e73251cc3a7
```
</details>

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

##### Example

```python
entropy = bytomHDWallet.generateEntropy()

bytomHDWallet, mnemonic = bytomHDWallet.masterKeyFromEntropy(entropy=entropy,
                                                             passphrase="meherett",
                                                             language="japanese")
print(mnemonic)
print(bytomHDWallet)
```
<details>
<summary>Output</summary>

```json5
たいむãおまいりãたんめいãきちょうãろんぶんãいなかãしなぎれãほえるãいもうとãひしょãじゆうãにんむ
<btmhdw.BytomHDWallet object at 0x7f3374618cf8>
```
</details>

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
