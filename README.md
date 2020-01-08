<p align="start">		
  <img src="https://raw.githubusercontent.com/meherett/btmhdw/master/btmhdw.png">		
</p>

# btmhdw

*The implementation of Hierarchical Deterministic (HD) wallets generator for Bytom blockchain.*

[![Build Status](https://travis-ci.org/meherett/btmhdw.svg?branch=master)](https://travis-ci.org/meherett/btmhdw)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/btmhdw.svg)
![PyPI License](https://img.shields.io/pypi/l/btmhdw.svg?color=black)
![PyPI Version](https://img.shields.io/pypi/v/btmhdw.svg?color=blue)
[![Coverage Status](https://coveralls.io/repos/github/meherett/btmhdw/badge.svg?branch=master)](https://coveralls.io/github/meherett/btmhdw?branch=master)

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
pytest tests
```
Or use `tox` to run the complete suite against the full set of build targets, or pytest to run specific 
tests against a specific version of Python.

## Usage
#### Create a new Bytom wallet
```python
from btmhdw import BTMHDW

# init BTMHDW
btmhdw = BTMHDW()

# Generate mnemonic english/japanese
mnemonic = btmhdw.generate_mnemonic("english")

# Checking mnemonic language
if not btmhdw.check_mnemonic(mnemonic, "english"):
    exit()

# Create a new wallet
wallet = btmhdw.create(mnemonic=mnemonic, network="mainnet")

print(wallet)
```
`OUTPUT`
```json5
{
  'mnemonic': 'gauge base climb fit output toast brave crush vacant predict hire remind',
  'address': 'bm1qn6g0tky8lx44j2ccz8cu88ngn4snfqr74d9ndw',
  'seed': 'b699dee73ef9be58fbf3490dab6e49071f96df97c5d2614a465b1fd3b76373f56edbac4e24b137f6226402e59902f0eaa882603f94b83618384500db1e30585b',
  'xprivate': '8007196f3e0841bbdf90d97df172a19cb18edda007466d362fa2d5ff23822a40189b8b295cc023e0b2c78f79725f859ac512afdfebc0b94cfd83faa59e42d82e',
  'xpublic': 'd47ece6097f93b5d19259886d210dab017f5b37520b4dad8160712fd5b1065e7189b8b295cc023e0b2c78f79725f859ac512afdfebc0b94cfd83faa59e42d82e',
  'program': '001468029bfd7635cec9100ed21ab6aee3a41986db71',
  'path': 'm/44/153/1/0/1',
}
```

#### Get wallet from XPrivate key
```python
from btmhdw import BTMHDW

XPRIVATE = "8007196f3e0841bbdf90d97df172a19cb18edda007466d362fa2d5ff23822a40189b8b295cc023e0b2c78f79725f859ac512afdfebc0b94cfd83faa59e42d82e"

# init BTMHDW
btmhdw = BTMHDW()

# Wallet from xprivate
wallet = btmhdw.wallet_from_xprivate(xprivate=XPRIVATE,
                                     network="mainnet")

print(wallet)
```
`OUTPUT`
```json5
{
  'address': 'bm1qn6g0tky8lx44j2ccz8cu88ngn4snfqr74d9ndw',
  'xprivate': '8007196f3e0841bbdf90d97df172a19cb18edda007466d362fa2d5ff23822a40189b8b295cc023e0b2c78f79725f859ac512afdfebc0b94cfd83faa59e42d82e',
  'xpublic': 'd47ece6097f93b5d19259886d210dab017f5b37520b4dad8160712fd5b1065e7189b8b295cc023e0b2c78f79725f859ac512afdfebc0b94cfd83faa59e42d82e', 
  'program': '001468029bfd7635cec9100ed21ab6aee3a41986db71',
  'path': 'm/44/153/1/0/1'
}
```

## Example
Here are more [btmhdw/example](https://github.com/meherett/btmhdw/blob/master/examples/example.py)

## Meta

Meheret Tesfaye – [@meherett](https://github.com/meherett) – meherett@zoho.com

Distributed under the MIT license. See ``LICENSE`` for more information.

[https://github.com/meherett](https://github.com/meherett) - *Initial work* - [Cobra](https://github.com/cobraframework)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details

## API

### Class BTMHDW()
**`generate_mnemonic()`**: It is to generate new mnemonic.

**Parameters**

`Optional`:
- `String` - *strength*, 128.
- `String` - *passphrase*, password of the key.
- `String` - *language*, mnemonic language of the key.

**Returns**

`Object`:
- `String` - *mnemonic*, generated mnemonic 12 words.

**Example**

```python
print(btmhdw.generate_mnemonic(language="english", passphrase="meherett"))
print(btmhdw.generate_mnemonic(language="japanese", passphrase="meherett"))
```
<details>
<summary>Output</summary>

```json5
"spare uniform possible grief attitude machine peace update tornado area evolve spread"
"あけがたãひていãぎじかがくãくうきãどうぐãだじゃれãおおうãりねんãこんだてãてわたしãはぶらしãちいき"
```
</details>

----

**`check_mnemonic()`**: It is to check mnemonic language.

**Parameters**

`Object`:
- `String` - *mnemonic*, mnemonic 12 words.

`Optional`:
- `String` - *language*, english/japanese by default english.

**Returns**

`Object`:
- `Boolean` - *boolean*, True/False.

**Example**

```python
MNEMONIC = "ancient young hurt bone shuffle deposit congress normal crack six boost despair"

print(btmhdw.check_mnemonic(MNEMONIC, "english"))
print(btmhdw.check_mnemonic(MNEMONIC, "japanese"))
```
<details>
<summary>Output</summary>

```python
True
False
```
</details>

----

**`generate_entropy()`**: It is to generate new entropy.

**Returns**

`Object`:
- `String` - *entropy*, generated entropy 32 length.

**Example**

```python
print(btmhdw.generate_entropy())
```
<details>
<summary>Output</summary>

```json5
"fbb9d20ec1fb94762b56dbc9cd184e23"
```
</details>

**`create()`**: It is to create new Bytom wallet.

**Parameters**

`Optional`:
- `String` - *mnemonic*, from mnemonic 12 words.
- `String` - *passphrase*, password of the key.
- `String` - *account*, account path index by default 1.
- `String` - *change*, change path index 0 or 1 by default 0.
- `String` - *address*, address path index by default 1.
- `String` - *path*, string of index.
- `Array` - *indexes*, array of index.
- `String` - *network*, mainnet(bm)/testnet(tm)/solonet(sm) by default sm.

**Returns**

`Object`:
- `Object` - *object*, keys are `entropy`, `mnemonic`, `address`, `seed`, `xprivate`, `xpublic`, `program` and `path`

**Example**

```python
mnemonic = btmhdw.generate_mnemonic("english")

createdWallet = btmhdw.create(mnemonic=mnemonic, 
                                    network="mainnet")
print(createdWallet['address'])
print(createdWallet['xprivate'], '\n')
print(createdWallet)
```
<details>
<summary>Output</summary>

```json5
"bm1qsv6u5z2uxtefnehkyuetyx4llu27umqscu8vtk"
"983fc70dc7c4a26ff9af39af4c0cc3057565b8f70a31158a6f37e1804ae6414ea6cade89861c53fafa461e5f0e116f47a816b11ba05585b79c577531c6000ffe" 

{
  'mnemonic': 'alarm fix day evoke void hawk pistol pulp impact farm average mask',
  'address': 'bm1qsv6u5z2uxtefnehkyuetyx4llu27umqscu8vtk',
  'seed': '6e269a33fb2c65b9a1966bc9579628869630d7d647792eaa3692fdae1db1a719ff4dfef17acf6027fb20ba7ce04e4715460ea2d280f69f646df1f2a6ef6ffea1',
  'xprivate': '983fc70dc7c4a26ff9af39af4c0cc3057565b8f70a31158a6f37e1804ae6414ea6cade89861c53fafa461e5f0e116f47a816b11ba05585b79c577531c6000ffe',
  'xpublic': '4a7bfcbccbe97aa3f92795c761697f98b6b2350597ab73c85109b025301db1aaa6cade89861c53fafa461e5f0e116f47a816b11ba05585b79c577531c6000ffe',
  'program': '0014312b5e9ee3625a50847ffd5244dbc0d8f01b8566',
  'path': 'm/44/153/1/0/1',
}
```
</details>

----

**`wallet_from_xprivate()`**: It is to get wallet from XPrivate

**Parameters**

`Object`:
- `String` - *xprivate*, xprivate key.

`Optional`:
- `String` - *account*, account path index by default 1.
- `String` - *change*, change path index 0 or 1 by default 0.
- `String` - *address*, address path index by default 1.
- `String` - *path*, string of index.
- `Array` - *indexes*, array of index.
- `String` - *network*, mainnet(bm)/testnet(tm)/solonet(sm) by default sm.

**Returns**

`Object`:
- `Object` - *object*, keys are `address`, `xprivate`, `xpublic`, `program` and `path`

**Example**

```python
XPRIVATE = "c003f4bcccf9ad6f05ad2c84fa5ff98430eb8e73de5de232bc29334c7d074759d513bc370335cac51d77f0be5dfe84de024cfee562530b4d873b5f5e2ff4f57c"

wallet_from_xprivate = btmhdw.wallet_from_xprivate(xprivate=XPRIVATE,
                                               network="mainnet")
print(wallet_from_xprivate['address'])
print(wallet_from_xprivate['xprivate'], '\n')
print(wallet_from_xprivate)
```
<details>
<summary>Output</summary>

```json5
"bm1qtzg058tt5eyf2qqfy2650erxqxhfkt4p236708"
"c003f4bcccf9ad6f05ad2c84fa5ff98430eb8e73de5de232bc29334c7d074759d513bc370335cac51d77f0be5dfe84de024cfee562530b4d873b5f5e2ff4f57c" 

{
  'address': 'bm1qtzg058tt5eyf2qqfy2650erxqxhfkt4p236708', 
  'xprivate': 'c003f4bcccf9ad6f05ad2c84fa5ff98430eb8e73de5de232bc29334c7d074759d513bc370335cac51d77f0be5dfe84de024cfee562530b4d873b5f5e2ff4f57c',
  'xpublic': '1b0541a7664cee929edb54d9ef21996b90546918a920a77e1cd6015d97c56563d513bc370335cac51d77f0be5dfe84de024cfee562530b4d873b5f5e2ff4f57c',
  'program': '0014dcf6b21d83c978d3125d1330c928c38fee315200',
  'path': 'm/44/153/1/0/1',
}
```
</details>

----

### Class BytomHDWallet()

**`master_key_from_mnemonic()`**: It is to get master key from mnemonic.

**Parameters**

`Object`:
- `String` - *mnemonic*, mnemonic 12 words.

`Optional`:
- `String` - *passphrase*, password of the key.

**Returns**

`Object`:
- `Object` - *BytomHDWallet*, class.

**Example**

```python
MNEMONIC = "ancient young hurt bone shuffle deposit congress normal crack six boost despair"

bytomHDWallet = BytomHDWallet.master_key_from_mnemonic(mnemonic=MNEMONIC,
                                                    passphrase="Meheret Tesfaye")
```

----

**`master_key_from_xprivate()`**: It is to get master key from XPrivate.

**Parameters**

`Object`:
- `String` - *xprivate*, xprivate key.

**Returns**

`Object`:
- `Object` - *BytomHDWallet*, class.

**Example**

```python
XPRIVATE = "c003f4bcccf9ad6f05ad2c84fa5ff98430eb8e73de5de232bc29334c7d074759d513bc370335cac51d77f0be5dfe84de024cfee562530b4d873b5f5e2ff4f57c"

bytomHDWallet = BytomHDWallet.master_key_from_xprivate(xprivate=XPRIVATE)
```

----

**`generate_entropy()`**: It is to generate new entropy.

**Returns**

`Object`:
- `String` - *entropy*, generated entropy.

**Example**

```python
print(bytomHDWallet.generate_entropy().hex())
```
<details>
<summary>Output</summary>

```json5
"7184af4506fb1b51c52d2e73251cc3a7"
```
</details>

----

**`master_key_from_entropy()`**: It is to get master key from mnemonic.

**Parameters**

`Optional`:
- `String` - *entropy*, from entropy.
- `String` - *strength*, 128.
- `String` - *passphrase*, password of the key.
- `String` - *language*, mnemonic language of the key.

**Returns**

`Object`:
- `Object` - *BytomHDWallet*, class.
- `String` - *mnemonic*, generated mnemonic 12 words.

**Example**

```python
entropy = bytomHDWallet.generate_entropy()

bytomHDWallet, mnemonic = bytomHDWallet.master_key_from_entropy(entropy=entropy,
                                                                passphrase="meherett",
                                                                language="japanese")
print(mnemonic)
print(bytomHDWallet)
```
<details>
<summary>Output</summary>

```json5
"たいむãおまいりãたんめいãきちょうãろんぶんãいなかãしなぎれãほえるãいもうとãひしょãじゆうãにんむ"
<btmhdw.BytomHDWallet object at 0x7f3374618cf8>
```
</details>

----

**`xprivate_key()`**: It is to get XPrivate key.

**Returns**

`Object`:
- `String` - *xprivate*, xprivate from master key.

**Example**

```python
MNEMONIC = "ancient young hurt bone shuffle deposit congress normal crack six boost despair"

bytomHDWallet = BytomHDWallet()
bytomHDWallet = bytomHDWallet.master_key_from_mnemonic(mnemonic=MNEMONIC)
bytomHDWallet.from_path("m/44/153/1/0/1")

print(bytomHDWallet.xprivate_key())
```
<details>
<summary>Output</summary>

```json5
"302a25c7c0a68a83fa043f594a2db8b44bc871fced553a8a33144b31bc7fb84887c9e75915bb6ba3fd0b9f94a60b7a5897ab9db6a48f888c2559132dba9152b0"
```
</details>

----

**`xpublic_key()`**: It is to get XPublic key.

**Parameters**

`Optional`:
- `String` - *xprivate*, from xprivate key.

**Returns**

`Object`:
- `String` - *xpublic*, xpublic from xprivate/master key.

**Example**

```python
XPRIVATE = "c003f4bcccf9ad6f05ad2c84fa5ff98430eb8e73de5de232bc29334c7d074759d513bc370335cac51d77f0be5dfe84de024cfee562530b4d873b5f5e2ff4f57c"

print(bytomHDWallet.xpublic_key(xprivate=XPRIVATE))
```
<details>
<summary>Output</summary>

```json5
"302a25c7c0a68a83fa043f594a2db8b44bc871fced553a8a33144b31bc7fb84887c9e75915bb6ba3fd0b9f94a60b7a5897ab9db6a48f888c2559132dba9152b0"
```
</details>

----

**`expand_xprivate_key()`**: It is to get Expand XPrivate key.

**Parameters**

`Optional`:
- `String` - *xprivate*, from xprivate key.

**Returns**

`Object`:
- `String` - *expandPrivate*, expand private key from xprivate/master key.

**Example**

```python
XPRIVATE = "c003f4bcccf9ad6f05ad2c84fa5ff98430eb8e73de5de232bc29334c7d074759d513bc370335cac51d77f0be5dfe84de024cfee562530b4d873b5f5e2ff4f57c"

print(bytomHDWallet.expand_xprivate_key(xprivate=XPRIVATE))
```
<details>
<summary>Output</summary>

```json5
"c003f4bcccf9ad6f05ad2c84fa5ff98430eb8e73de5de232bc29334c7d074759b47fcbbf006db960004839862e694fb3647fdc081ae109bbfe3b07de83e39807"
```
</details>

----

**`public_key()`**: It is to get public key(length 64).

**Parameters**

`Optional`:
- `String` - *xpublic*, from xpublic key.

**Returns**

`Object`:
- `String` - *public*, public key(length 64) from xpublic/master key.

**Example**

```python
XPUBLIC = "3c6664244d2d57168d173c4691dbf8741a67d972b2d3e1b0067eb825e2005d20c5eebd1c26ccad4de5142d7c339bf62cc1fb79a8b3e42a708cd521368dbc9286"

print(bytomHDWallet.public_key(xpublic=XPUBLIC))
```
<details>
<summary>Output</summary>

```json5
"3c6664244d2d57168d173c4691dbf8741a67d972b2d3e1b0067eb825e2005d20"
```
</details>

----

**`from_indexes()`**: It is to set collection of index.

**Parameters**

`Object`:
- `Array` - *indexes*, array of index.

**Returns**

`Object`:
- `Object` - *BytomHDWallet*, class.

**Example**

```python
INDEXES = ['2c000000', '99000000', '01000000', '01000000', '99000000']

bytomHDWallet = bytomHDWallet.from_indexes(indexes=INDEXES)
```

----

**`from_index()`**: It is to set index.

**Parameters**

`Object`:
- `Number` - *index*, number.

**Returns**

`Object`:
- `Object` - *BytomHDWallet*, class.

**Example**

```python
bytomHDWallet = BytomHDWallet()

bytomHDWallet.from_index(44)
bytomHDWallet.from_index(153)
bytomHDWallet.from_index(1)  # account
bytomHDWallet.from_index(0)  # change 0 or 1
bytomHDWallet.from_index(1)  # address

# Advanced BTMHDW_HARDEN

bytomHDWallet.from_index(44)
bytomHDWallet.from_index(153 + BTMHDW_HARDEN)
bytomHDWallet.from_index(1 + BTMHDW_HARDEN)
bytomHDWallet.from_index(0)
bytomHDWallet.from_index(1)
```

----

**`from_path()`**: It is to set index from path.

**Parameters**

`Object`:
- `String` - *path*, string of index.

**Returns**

`Object`:
- `Object` - *BytomHDWallet*, class.

**Example**

```python
bytomHDWallet = BytomHDWallet()

bytomHDWallet.from_path("m/44/153/1/0/1")

# Advanced BTMHDW_HARDEN using "'"

bytomHDWallet.from_path("m/44/153'/1'/0/1")
```

----

**`get_indexes()`**: It is to get collection of index.

**Returns**

`Object`:
- `Array` - *indexes*, collection of index.

**Example**

```python
print(bytomHDWallet.get_indexes())
```
<details>
<summary>Output</summary>

```json5
['2c000000', '99000000', '01000000', '01000000', '99000000']
```
</details>

----

**`get_path()`**: It is to get path of indexes.

**Parameters**

`Optional`:
- `String` - *indexes*, from array of index.

**Returns**

`Object`:
- `String` - *path*, string of index from indexes/master key.

**Example**

```python
from btmhdw import INDEXES

print(bytomHDWallet.get_path(indexes=INDEXES))
```
<details>
<summary>Output</summary>

```json5
"m/44/153/1/0/1"
```
</details>

----

**`child_xprivate_key()`**: It is to get child of XPrivate key.

**Parameters**

`Optional`:
- `String` - *xprivate*, from xprivate key.
- `String` - *indexes*, collection of index.

**Returns**

`Object`:
- `String` - *childXPrivate*, child xprivate key from xprivate/indexes/master key.

**Example**

```python
from btmhdw import INDEXES

XPRIVATE = "c003f4bcccf9ad6f05ad2c84fa5ff98430eb8e73de5de232bc29334c7d074759d513bc370335cac51d77f0be5dfe84de024cfee562530b4d873b5f5e2ff4f57c"

child_xprivate_key = bytomHDWallet.child_xprivate_key(xprivate=XPRIVATE,
                                                      indexes=INDEXES)
print(child_xprivate_key)
```
<details>
<summary>Output</summary>

```json5
"d01acc504811886d732ea6ea19c066b0f1fb4d0b2a0b97414d1d3916c70c47596aca269da2343d4d7588ffa3c8b9244a156748276114e5f2b86fa69ec241b62a"
```
</details>

----

**`sing()`**: Singing message.

**Parameters**

`Object`:
- `String` - *message*, message to sing.

`Optional`:
- `String` - *xprivate*, xprivate key.

**Returns**

`Object`:
- `String` - *signature*, signed message.

**Example**

```python

MESSAGE = "27c42b40a7a35a6d489fb2e41bde15bdb4b4c276045bd0628525b88c2abbc4c0"

signature = bytomHDWallet.sign(message=MESSAGE)

print(signature)
```
<details>
<summary>Output</summary>

```json5
"75ca5b6cf7ba40c7a51f20e1fd03686666e09cf58d0d2978ab6072d8057cbbd3072eabbdefe96eefcbb0c8ec654239b82fa5efcbe24e8704c7d06efd79c40d0a"
```
</details>

----

**`verify()`**: Verifying signed message.

**Parameters**

`Object`:
- `String` - *message*, message to sing.
- `String` - *signature*, signed message.

`Optional`:
- `String` - *xpublic*, xpublic key.

**Returns**

`Object`:
- `Boolean` - *bool*, true or false.

**Example**

```python
MESSAGE = "27c42b40a7a35a6d489fb2e41bde15bdb4b4c276045bd0628525b88c2abbc4c0"

verify_signature = bytomHDWallet.verify(message=MESSAGE, signature=signature)

print(verify_signature)
```
<details>
<summary>Output</summary>

```python
True
```
</details>

----

**`child_xpublic_key()`**: It is to get child of XPublic key.

**Parameters**

`Optional`:
- `String` - *xpublic*, from xpublic key.
- `String` - *indexes*, collection of index.

**Returns**

`Object`:
- `String` - *child_xpublic_key*, child xpublic key from xpublic/indexes/master key.

**Example**

```python
from btmhdw import INDEXES

XPUBLIC = "3c6664244d2d57168d173c4691dbf8741a67d972b2d3e1b0067eb825e2005d20c5eebd1c26ccad4de5142d7c339bf62cc1fb79a8b3e42a708cd521368dbc9286"

child_xpublic_key = bytomHDWallet.child_xpublic_key(xpublic=XPUBLIC,
                                                    indexes=INDEXES)
print(child_xpublic_key)
```
<details>
<summary>Output</summary>

```json5
"e87ca3acdebdcad9a1d0f2caecf8ce0dbfc73d060807a210c6f2254883479614bcde9cf9e8ee322097d639b33b398c2e419de4092409bf43b3632ddefc4beae9"
```
</details>

----

**`program()`**: It is to get control program.

**Parameters**

`Optional`:
- `String` - *xpublic*, from xpublic key.
- `String` - *path*, path of index.
- `String` - *indexes*, collection of index.

**Returns**

`Object`:
- `String` - *program*, control program from xpublic/master key.

**Example**
```python
from btmhdw import INDEXES, PATH

# Getting contract Program from xpublic and path or indexes
print(BytomHDWallet().program(xpublic=XPUBLIC, path="m/44/153/2/0/8"))
print(BytomHDWallet().program(xpublic=XPUBLIC, path=PATH))
print(BytomHDWallet().program(xpublic=XPUBLIC, indexes=INDEXES))
print(BytomHDWallet().program(xpublic=XPUBLIC, indexes=['2c000000', '99000000', '01000000', '01000000', '01000000']))
print(BytomHDWallet().program(public=PUBLIC))
```
<details>
<summary>Output</summary>

```json5
"00140afb404c13a122306ee86f5ff9b177334d8e23b7"
"0014052620b86a6d5e07311d5019dffa3864ccc8a6bd"
"00140afb404c13a122306ee86f5ff9b177334d8e23b7"
"0014052620b86a6d5e07311d5019dffa3864ccc8a6bd"
"001478c3aa31753389fcde04d33d0779bdc2840f0ad4"
```
</details>

----

**`address()`**: It is to get address.

**Parameters**

`Optional`:
- `String` - *program*, from control program.
- `String` - *network*, mainnet(bm)/testnet(tm)/solonet(sm) by default sm.

**Returns**

`Object`:
- `String` - *address*, address from control program/master key.

**Example**

```python
XPUBLIC = "3c6664244d2d57168d173c4691dbf8741a67d972b2d3e1b0067eb825e2005d20c5eebd1c26ccad4de5142d7c339bf62cc1fb79a8b3e42a708cd521368dbc9286"

program = BytomHDWallet().program(xpublic=XPUBLIC, path="m/44/153/2/0/8")
print(bytomHDWallet.address(program=program,
                            network='mainnet'))  # or network bm
print(bytomHDWallet.address(program=program,
                            network='testnet'))  # or network tm
print(bytomHDWallet.address(program=program,
                            network='solonet'))  # or network sm
```
<details>
<summary>Output</summary>

```json5
"bm1qpta5qnqn5y3rqmhgda0lnvthxdxcugahcpaum5"
"tm1qpta5qnqn5y3rqmhgda0lnvthxdxcugahuhucm9"
"sm1qpta5qnqn5y3rqmhgda0lnvthxdxcugahesham6"
```
</details>

----

### Extra Functions

**`sing()`**: Singing message.

**Parameters**

`Object`:
- `String` - *message*, message to sing.
- `String` - *xprivate*, xprivate key.

**Returns**

`Object`:
- `String` - *signature*, signed message.

**Example**

```python
from btmhdw import sign

MESSAGE = "27c42b40a7a35a6d489fb2e41bde15bdb4b4c276045bd0628525b88c2abbc4c0"
XPRIVATE = "302a25c7c0a68a83fa043f594a2db8b44bc871fced553a8a33144b31bc7fb84887c9e75915bb6ba3fd0b9f94a60b7a5897ab9db6a48f888c2559132dba9152b0"

signature = sign(message=MESSAGE, xprivate=XPRIVATE)

print(signature)
```
<details>
<summary>Output</summary>

```json5
"a39045f6c8b87b3adce39057e448b37c2300bb3dfce0d8b6034a28bbcccfa4353fc23cb158a310990205fed302bbdfa64255b49f7b1eb2fb502756f164922309"
```
</details>

----

**`verify()`**: Verifying signed message.

**Parameters**

`Object`:
- `String` - *message*, message to sing.
- `String` - *signature*, signed message.
- `String` - *xpublic*, xpublic key.

**Returns**

`Object`:
- `Boolean` - *bool*, true or false.

**Example**

```python
from btmhdw import verify

MESSAGE = "27c42b40a7a35a6d489fb2e41bde15bdb4b4c276045bd0628525b88c2abbc4c0"
SIGNATURE = "a39045f6c8b87b3adce39057e448b37c2300bb3dfce0d8b6034a28bbcccfa4353fc23cb158a310990205fed302bbdfa64255b49f7b1eb2fb502756f164922309"
XPUBLIC = "9407d490e9dbc7762c924122368e6c5743d5829ff2a1e2eb4b219a08e080499687c9e75915bb6ba3fd0b9f94a60b7a5897ab9db6a48f888c2559132dba9152b0"

verify_signature = verify(message=MESSAGE, signature=SIGNATURE, xpublic=XPUBLIC)

print(verify_signature)
```
<details>
<summary>Output</summary>

```python
True
```
</details>
