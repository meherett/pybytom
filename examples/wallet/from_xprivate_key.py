#!/usr/bin/env python3

from pybytom.wallet import Wallet
from pybytom.assets import BTM as ASSET
from pybytom.utils import amount_converter

import json

# Choose network mainnet, solonet or testnet
NETWORK: str = "mainnet"  # Default is mainnet
# Bytom xprivate key
XPRIVATE_KEY: str = "3842e3fa2af2a687e7fd67655e7a02e85bbb4ca378d4338ff590dedc7ddff447797" \
                    "e1e781190835138c2d1a96d0e654b625a4c019cbc64f71100be7ad1b8d4ed"
# Message data
MESSAGE: str = "a0841d35364046649ab8fc4af5a6266245890778f6cf7304696c4ab8edd86242"

# Initialize Bytom wallet
wallet: Wallet = Wallet(network=NETWORK)
# Get Bytom wallet xprivate key
wallet.from_xprivate_key(xprivate_key=XPRIVATE_KEY)

# Derivation from path
# wallet.from_path("m/44/153/1/0/1")
# Or derivation from index
# wallet.from_index(44)
# wallet.from_index(153)
# wallet.from_index(1)
# wallet.from_index(0)
# wallet.from_index(1)
# Or derivation from indexes
wallet.from_indexes(["2c000000", "99000000", "01000000", "00000000", "01000000"])

# Print all wallet information's
# print(json.dumps(wallet.dumps(), indent=4, ensure_ascii=False))

print("XPrivate Key:", wallet.xprivate_key())
print("Expand XPrivate Key:", wallet.expand_xprivate_key())
print("XPublic Key:", wallet.xpublic_key())
# print("GUID:", wallet.guid())
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
print("UTXO's:", wallet.utxos(asset=ASSET, vapor=False))
print("Vapor UTXO's:", wallet.utxos(asset=ASSET, vapor=True))

print("-------- Sign & Verify --------")

print("Message:", MESSAGE)
signature = wallet.sign(message=MESSAGE)
print("Signature:", signature)
print("Verified:", wallet.verify(message=MESSAGE, signature=signature))
