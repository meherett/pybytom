#!/usr/bin/env python3

from pybytom.wallet import Wallet
from pybytom.utils import generate_entropy, amount_converter
from pybytom.assets import BTM as ASSET
from typing import Optional

import json

# Choose network mainnet, solonet or testnet
NETWORK: str = "mainnet"  # Default is mainnet
# Choose strength 128, 160, 192, 224 or 256
STRENGTH: int = 224  # Default is 128
# Choose language english, french, italian, spanish, chinese_simplified, chinese_traditional, japanese or korean
LANGUAGE: str = "japanese"  # Default is english
# Generate new entropy seed
ENTROPY: str = generate_entropy(strength=STRENGTH)
# Secret passphrase/password for mnemonic
PASSPHRASE: Optional[str] = None  # str("meherett")
# Message data
MESSAGE: str = "a0841d35364046649ab8fc4af5a6266245890778f6cf7304696c4ab8edd86242"

# Initialize Bytom wallet
wallet: Wallet = Wallet(network=NETWORK)
# Get Bytom wallet from entropy
wallet.from_entropy(
    entropy=ENTROPY, passphrase=PASSPHRASE, language=LANGUAGE
)

# Derivation from path
# wallet.from_path("m/44/153/1/0/1")
# Or derivation from index
wallet.from_index(44)
wallet.from_index(153)
wallet.from_index(1)
wallet.from_index(0)
wallet.from_index(1)
# Or derivation from indexes
# wallet.from_indexes(["2c000000", "99000000", "01000000", "00000000", "01000000"])

# Print all wallet information's
# print(json.dumps(wallet.dumps(), indent=4, ensure_ascii=False))

print("Strength:", wallet.strength())
print("Entropy:", wallet.entropy())
print("Mnemonic:", wallet.mnemonic())
print("Language:", wallet.language())
print("Passphrase:", wallet.passphrase())
print("Seed:", wallet.seed())
print("XPrivate Key:", wallet.xprivate_key())
print("Expand XPrivate Key:", wallet.expand_xprivate_key())
print("XPublic Key:", wallet.xpublic_key())
print("GUID:", wallet.guid())
print("Indexes:", wallet.indexes())
print("Path:", wallet.path())
print("Child XPrivate Key:", wallet.child_xprivate_key())
print("Child XPublic Key:", wallet.child_xpublic_key())
print("Private Key:", wallet.private_key())
print("Public Key:", wallet.public_key())
print("Program:", wallet.program())
print("Address:", wallet.address(vapor=False))
print("Vapor Address:", wallet.address(vapor=True))
print("Balance:", amount_converter(wallet.balance(asset=ASSET, vapor=False), "NEU2BTM"), "BTM")
print("Vapor Balance:", amount_converter(wallet.balance(asset=ASSET, vapor=True), "NEU2BTM"), "BTM")
print("UTXO's:", wallet.utxos(asset=ASSET))

print("-------- Sign & Verify --------")

print("Message:", MESSAGE)
signature: str = wallet.sign(message=MESSAGE)
print("Signature:", signature)
print("Verified:", wallet.verify(message=MESSAGE, signature=signature))
