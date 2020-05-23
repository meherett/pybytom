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

# Choose strength 128, 160, 192, 224 or 256
ENTROPY = generate_entropy(strength=128)  # Default is 128
# Secret password/passphrase
PASSPHRASE = None  # str("meherett")
# Choose language english, french, italian, spanish, chinese_simplified, chinese_traditional, japanese or korean
LANGUAGE = "chinese_traditional"  # Default is english

# Initialize wallet
wallet = Wallet(network="mainnet")  # Choose network mainnet, solonet or testnet 
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
print(json.dumps(wallet.dumps(guid=True), indent=4, ensure_ascii=False))
```

<details>
  <summary>Output</summary><br/>

```json5
{
    "entropy": "bd616c3c32046eceb490cc79730176b4",
    "mnemonic": "恐 體 那 訓 魚 謂 襲 設 苗 嘴 刻 鐘",
    "language": "chinese_traditional",
    "passphrase": null,
    "seed": "8caf7c485297a6618db6cdaa2e701d787768a84f1fc004cabc9628dec6d00560d7a7955e371392272e032bed5ffc368359e5b1f396c609820791e1b367ec9f6d",
    "xprivate_key": "28ec473e78705d3ea4d95f5671f98a64b788b6155553df3e723a7157cadf6453a9d90389fa964b9bad8741647a7a3d783681514fa24e21d17afc3aa1d84de959",
    "xpublic_key": "76436d956e5d2d81633b4fe201c99c9b270dcb962bf8d22e1bb43c8c38413ef5a9d90389fa964b9bad8741647a7a3d783681514fa24e21d17afc3aa1d84de959",
    "expand_xprivate_key": "28ec473e78705d3ea4d95f5671f98a64b788b6155553df3e723a7157cadf64535dee8b97f73c512fac7b11d3caf72c67d5250d1f73f017212e89f9dac33f5515",
    "guid": "22a71cb7-bfee-48bf-93e9-756bbe194737",
    "indexes": ["2c000000", "99000000", "2f000000", "3d000000", "59000000"],
    "path": "m/44/153/47/61/89",
    "child_xprivate_key": "103ff6f6da30d868dcec4b14538501c0ea2cdc878c0522697261b10218e46453bbbb0601dd6625749235b02625150ee6d363ce67c07b6d3987d92957433a140d",
    "child_xpublic_key": "5b5a06f6fbcb74b58ebb42293808fec6222234df6c97d7c1cff6d857a6024dc2bbbb0601dd6625749235b02625150ee6d363ce67c07b6d3987d92957433a140d",
    "private_key": "103ff6f6da30d868dcec4b14538501c0ea2cdc878c0522697261b10218e46453bbbb0601dd6625749235b02625150ee6d363ce67c07b6d3987d92957433a140d",
    "public_key": "5b5a06f6fbcb74b58ebb42293808fec6222234df6c97d7c1cff6d857a6024dc2",
    "program": "0014875240ba66646d900c59dd20d843351c2fcbeedc",
    "address": {
        "mainnet": "bm1qsafypwnxv3keqrzem5sdsse4rshuhmku7kpnxq",
        "solonet": "sm1qsafypwnxv3keqrzem5sdsse4rshuhmkul8tjxw",
        "testnet": "tm1qsafypwnxv3keqrzem5sdsse4rshuhmku6qqhx3"
    },
    "vapor_address": {
        "mainnet": "vp1qsafypwnxv3keqrzem5sdsse4rshuhmku4h3wrk",
        "solonet": "sp1qsafypwnxv3keqrzem5sdsse4rshuhmkuajnxra",
        "testnet": "tp1qsafypwnxv3keqrzem5sdsse4rshuhmkuc4crrz"
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
wallet = Wallet(network="mainnet")  # Choose network mainnet, solonet or testnet 
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
    # Print account_index, change, address_index, address and private_key like bytom core wallet accounts
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
print(f"Signature: {signature}")

# Verify signature by public key
print(f"Verified: {verify(public_key=PUBLIC_KEY, signature=signature, message=MESSAGE)}")
```

<details>
  <summary>Output</summary><br/>

```shell script
Signature: f6624fea84fadccbc1bc72dc384f662468e271c4e32d846bc0a1524470549992c8ffcc3ca43891a30de4235392b0868c506ed254f0f77cc1f2b9c1a2385ddb05
Verified: True
```
</details>

bytom normal transaction

```python
#!/usr/bin/env python3

from pybytom.transaction import NormalTransaction
from pybytom.rpc import submit_transaction_raw
from pybytom.wallet import Wallet

# Bytom network and 12 word mnemonic
NETWORK, MNEMONIC = "mainnet", "indicate warm sock mistake code spot acid ribbon sing over taxi toast"

# Initializing sender wallet from mnemonic and derivation from path
wallet = Wallet(network=NETWORK).from_mnemonic(mnemonic=MNEMONIC).from_path(path="m/44/153/1/0/1")

# Initializing normal transaction and building transaction
normal_transaction = NormalTransaction(network=NETWORK).build_transaction(
    guid=wallet.guid(),
    recipients={
        "bm1qzx7pjr6whcaxmh9u0thkjuavf2ynk3zkgshhle": 10_000_000,  # recipient 1
        "bm1q8wjwl5pxava9zgukf0sadqm5ec2aq0kt84hpxn": 90_000_000   # recipient 2
    },
    asset="ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff"
)

# Print transaction info's
print(f"Normal Transaction Fee: {normal_transaction.fee()}")
print(f"Normal Transaction Confirmations: {normal_transaction.confirmations()}")
print(f"Normal Transaction Hash: {normal_transaction.hash()}")
print(f"Normal Transaction Raw: {normal_transaction.raw()}")
print(f"Normal Transaction Json: {normal_transaction.json()}")
print(f"Normal Transaction Unsigned Datas: {normal_transaction.unsigned_datas(detail=False)}")

# Print before signing transaction signatures
print(f"\nBefore Signing Normal Transaction Signatures: {normal_transaction.signatures()}")
# Singing datas
normal_transaction.sign(
    xprivate_key=wallet.xprivate_key(),
)
# Print after signed transaction signatures
print(f"After Signed Normal Transaction Signatures: {normal_transaction.signatures()}")

# Submitting transaction raw
print("\nSubmitted Bytom Blockchain Transaction Hash:", submit_transaction_raw(
    guid=wallet.guid(), 
    transaction_raw=normal_transaction.raw(),
    signatures=normal_transaction.signatures(),
    network=NETWORK
))
```

<details>
  <summary>Output</summary><br/>

```shell script
Normal Transaction Fee: 10000000
Normal Transaction Confirmations: 1
Normal Transaction Hash: 72868fe4134bb2e58c67e1c67a71c5bbed5bf8259e8405203d95a70294ea0629
Normal Transaction Raw: 070100010160015eeef93f1d43b10b7cb076603f706a69dcfb7b0637b4a747153f5240516861f2defffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff08fb7e40801011600142cda4f99ea8112e6fa61cdd26157ed6dc408332a22012091ff7f525ff40874c4f47f0cab42e46e3bf53adad59adef9558ad1b6448f22e203013cffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff80ade2040116001411bc190f4ebe3a6ddcbc7aef6973ac4a893b445600013cffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff8095f52a011600143ba4efd026eb3a5123964be1d68374ce15d03ecb00013dfffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff0a0fdaf08011600142cda4f99ea8112e6fa61cdd26157ed6dc408332a00
Normal Transaction Json: {'hash': '72868fe4134bb2e58c67e1c67a71c5bbed5bf8259e8405203d95a70294ea0629', 'status_fail': False, 'size': 328, 'submission_timestamp': 0, 'memo': '', 'inputs': [{'script': '00142cda4f99ea8112e6fa61cdd26157ed6dc408332a', 'address': 'bm1q9ndylx02syfwd7npehfxz4lddhzqsve2fu6vc7', 'asset': 'ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff', 'amount': 2358102000, 'type': 'spend'}], 'outputs': [{'utxo_id': '80a8cda6741c28921964c71a00d79531f068aa92e10ad36b113fc81927eed268', 'script': '001411bc190f4ebe3a6ddcbc7aef6973ac4a893b4456', 'address': 'bm1qzx7pjr6whcaxmh9u0thkjuavf2ynk3zkgshhle', 'asset': 'ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff', 'amount': 10000000, 'type': 'control'}, {'utxo_id': '1495fa02229be717fb749525678325c394fc50ad5dd88929003d11b5ccc05720', 'script': '00143ba4efd026eb3a5123964be1d68374ce15d03ecb', 'address': 'bm1q8wjwl5pxava9zgukf0sadqm5ec2aq0kt84hpxn', 'asset': 'ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff', 'amount': 90000000, 'type': 'control'}, {'utxo_id': '844d6ba91489d05afc2f17e5c2148c1a28901af13b531ff6c91df07a85ba5950', 'script': '00142cda4f99ea8112e6fa61cdd26157ed6dc408332a', 'address': 'bm1q9ndylx02syfwd7npehfxz4lddhzqsve2fu6vc7', 'asset': 'ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff', 'amount': 2248102000, 'type': 'control'}], 'fee': 10000000, 'balances': [{'asset': 'ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff', 'amount': '-110000000'}], 'types': ['ordinary']}
Normal Transaction Unsigned Datas: [{'datas': ['10f96b2eaa037d06cd5022ea50b8f184203c6ba1565a0618d19e3c8de3715c56'], 'public_key': '91ff7f525ff40874c4f47f0cab42e46e3bf53adad59adef9558ad1b6448f22e2', 'network': 'mainnet', 'path': 'm/44/153/1/0/1'}]

Before Signing Normal Transaction Signatures: []
After Signed Normal Transaction Signatures: [['1648308c6961ed17d27bddeb0fd5289b56b2abe1c9511fe3a535fd75d4319ad8aeefbf859015cc242707c1377ad5c45de0d8de6201d86d0bff773f9079474706']]

Submitted Bytom Blockchain Transaction Hash: 72868fe4134bb2e58c67e1c67a71c5bbed5bf8259e8405203d95a70294ea0629
```
</details>

bytom advanced transaction

```python
#!/usr/bin/env python3

from pybytom.transaction import AdvancedTransaction
from pybytom.transaction.tools import find_contract_utxo_id, spend_utxo_action, control_address_action
from pybytom.rpc import submit_transaction_raw
from pybytom.wallet import Wallet

# Bytom network and 12 word mnemonic
NETWORK, MNEMONIC = "mainnet", "indicate warm sock mistake code spot acid ribbon sing over taxi toast"

# Initializing sender wallet from mnemonic and driving from path
wallet = Wallet(network=NETWORK).from_mnemonic(mnemonic=MNEMONIC).from_path(path="m/44/153/1/0/1")

# Initializing advanced transaction and building transaction
advanced_transaction = AdvancedTransaction(network=NETWORK).build_transaction(
    guid=wallet.guid(),
    inputs=[
        spend_utxo_action(
            utxo=find_contract_utxo_id(
                transaction_id="338cf2a29f055289132dd0f75d2d82777d2db1c7dbe64700cd24b03912e5d8e3",
                network=NETWORK
            )
        )
    ],
    outputs=[
        control_address_action(
            asset="f37dea62efd2965174b84bbb59a0bd0a671cf5fb2857303ffd77c1b482b84bdf",
            amount=100,
            address=wallet.address()
        )
    ],
    fee=10_000_000,
    confirmations=1
)

# Print transaction info's
print(f"Advanced Transaction Fee: {advanced_transaction.fee()}")
print(f"Advanced Transaction Confirmations: {advanced_transaction.confirmations()}")
print(f"Advanced Transaction Hash: {advanced_transaction.hash()}")
print(f"Advanced Transaction Raw: {advanced_transaction.raw()}")
print(f"Advanced Transaction Json: {advanced_transaction.json()}")
print(f"Advanced Transaction Unsigned Datas: {advanced_transaction.unsigned_datas(detail=False)}")

# Print before signing transaction signatures
print(f"\nBefore Signing Advanced Transaction Signatures: {advanced_transaction.signatures()}")
# Singing datas
advanced_transaction.sign(
    xprivate_key=wallet.xprivate_key(),
    indexes=["2c000000", "99000000", "01000000", "00000000", "01000000"]
)
# Print after signed transaction signatures
print(f"After Signed Advanced Transaction Signatures: {advanced_transaction.signatures()}")

# Submitting transaction raw
print("\nSubmitted Bytom Blockchain Transaction Hash:", submit_transaction_raw(
    guid=wallet.guid(), 
    transaction_raw=advanced_transaction.raw(),
    signatures=advanced_transaction.signatures(),
    network=NETWORK
))
```

<details>
  <summary>Output</summary><br/>

```shell script
Advanced Transaction Fee: 10000000
Advanced Transaction Confirmations: 1
Advanced Transaction Hash: 70c4af34a360a9e4e88d4bd77883df4ab381e67d9c7960919bb118cb4b91bafc
Advanced Transaction Raw: 0701000201d00101cd0139630abd345a77b9112aac3c554a788a28cfb3e3015222ba058cfc751cbefa90f37dea62efd2965174b84bbb59a0bd0a671cf5fb2857303ffd77c1b482b84bdf640001880101642091ff7f525ff40874c4f47f0cab42e46e3bf53adad59adef9558ad1b6448f22e220ac13c0bb1445423a641754182d53f0677cd4351a0e743e6f10b35122c3d7ea01203a26da82ead15a80533a02696656b14b5dbfd84eb14790f2e1be5e9e45820eeb741f547a6416000000557aa888537a7cae7cac631f000000537acd9f6972ae7cac00c001000160015e39630abd345a77b9112aac3c554a788a28cfb3e3015222ba058cfc751cbefa90fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff0e2d4df0802011600142cda4f99ea8112e6fa61cdd26157ed6dc408332a22012091ff7f525ff40874c4f47f0cab42e46e3bf53adad59adef9558ad1b6448f22e2020139f37dea62efd2965174b84bbb59a0bd0a671cf5fb2857303ffd77c1b482b84bdf64011600142cda4f99ea8112e6fa61cdd26157ed6dc408332a00013dfffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff0b5f2da08011600142cda4f99ea8112e6fa61cdd26157ed6dc408332a00
Advanced Transaction Json: {'hash': '70c4af34a360a9e4e88d4bd77883df4ab381e67d9c7960919bb118cb4b91bafc', 'status_fail': False, 'size': 475, 'submission_timestamp': 0, 'memo': '', 'inputs': [{'script': '01642091ff7f525ff40874c4f47f0cab42e46e3bf53adad59adef9558ad1b6448f22e220ac13c0bb1445423a641754182d53f0677cd4351a0e743e6f10b35122c3d7ea01203a26da82ead15a80533a02696656b14b5dbfd84eb14790f2e1be5e9e45820eeb741f547a6416000000557aa888537a7cae7cac631f000000537acd9f6972ae7cac00c0', 'address': 'smart contract', 'asset': 'f37dea62efd2965174b84bbb59a0bd0a671cf5fb2857303ffd77c1b482b84bdf', 'amount': 100, 'type': 'spend'}, {'script': '00142cda4f99ea8112e6fa61cdd26157ed6dc408332a', 'address': 'bm1q9ndylx02syfwd7npehfxz4lddhzqsve2fu6vc7', 'asset': 'ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff', 'amount': 2348102000, 'type': 'spend'}], 'outputs': [{'utxo_id': '4f871cbbfdfecdbed4075fe027e39850f80797f23b5036168d393739ca0e95a1', 'script': '00142cda4f99ea8112e6fa61cdd26157ed6dc408332a', 'address': 'bm1q9ndylx02syfwd7npehfxz4lddhzqsve2fu6vc7', 'asset': 'f37dea62efd2965174b84bbb59a0bd0a671cf5fb2857303ffd77c1b482b84bdf', 'amount': 100, 'type': 'control'}, {'utxo_id': 'fb72ff773c6b5274acad7a6794d77204be94857f159d4ba3d03a0381c645cc6e', 'script': '00142cda4f99ea8112e6fa61cdd26157ed6dc408332a', 'address': 'bm1q9ndylx02syfwd7npehfxz4lddhzqsve2fu6vc7', 'asset': 'ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff', 'amount': 2338102000, 'type': 'control'}], 'fee': 10000000, 'balances': [{'asset': 'ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff', 'amount': '-10000000'}, {'asset': 'f37dea62efd2965174b84bbb59a0bd0a671cf5fb2857303ffd77c1b482b84bdf', 'amount': '100'}], 'types': ['ordinary']}
Advanced Transaction Unsigned Datas: [{'datas': ['6eeef43c62eb90d2585e4e0128a671d6b5efe6f0645c288372e5335696d3db2a'], 'network': 'mainnet', 'path': None}, {'datas': ['eab36e3689be0fd72f0c11f44a2260b2676bf3f3b27f3d4d8ffb893278ed90ca'], 'public_key': '91ff7f525ff40874c4f47f0cab42e46e3bf53adad59adef9558ad1b6448f22e2', 'network': 'mainnet', 'path': 'm/44/153/1/0/1'}]

Before Signing Advanced Transaction Signatures: []
After Signed Advanced Transaction Signatures: [['efcb400b08eec8e263e18f449d0104ec04917baced977795660f75a12ee5b7bab16c4b5df4918388f5dec0a82f23564d0fc6aa9fee4ad0858117077b5b06330d'], ['004f39908afeedadc107d0deb6da2a250292bfbad1a94c3ae23de641a90cce32210c2ba549240752f4b503438b167331bfc311d3257c78f00ca4137acc83290d']]

Submitted Bytom Blockchain Transaction Hash: 70c4af34a360a9e4e88d4bd77883df4ab381e67d9c7960919bb118cb4b91bafc
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
