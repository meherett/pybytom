#!/usr/bin/env python3

from pybytom.wallet import Wallet

import json

# Wallet seed
SEED = "b3337a2fe409afbb257b504e4c09d36b57c32c452b71a0ed413298a5172f727a06bf6605488" \
       "723bc545a4bd51f5cd29a3e8bd1433bd1d26e6bf866ff53d1493f"

# Message data
MESSAGE = "a0841d35364046649ab8fc4af5a6266245890778f6cf7304696c4ab8edd86242"

# Initialize wallet
wallet = Wallet(network="mainnet")
# Get Bytom wallet from seed
wallet.from_seed(seed=SEED)

# Derivation from path
wallet.from_path("m/44/153/1/0/1")
# Or derivation from index
# wallet.from_index(44)
# wallet.from_index(153)
# wallet.from_index(1)
# wallet.from_index(0)
# wallet.from_index(1)
# Or derivation from indexes
# wallet.from_indexes(['2c000000', '99000000', '01000000', '00000000', '01000000'])

# Print all wallet information's
# print(json.dumps(wallet.dumps(), indent=4))

print("Entropy:", wallet.entropy())
print("Mnemonic:", wallet.mnemonic())
print("Language:", wallet.language())
print("Passphrase:", wallet.passphrase())
print("Seed:", wallet.seed())
print("XPrivate Key:", wallet.xprivate_key())
print("Expand XPrivate Key:", wallet.expand_xprivate_key())
print("XPublic Key:", wallet.xpublic_key())
print("Indexes:", wallet.indexes())
print("Path:", wallet.path())
print("Child XPrivate Key:", wallet.child_xprivate_key())
print("Child XPublic Key:", wallet.child_xpublic_key())
print("Private Key:", wallet.private_key())
print("Public Key:", wallet.public_key())
print("Program:", wallet.program())
print("Address:", wallet.address())

print("-------- Sign & Verify --------")

print("Message:", MESSAGE)
signature = wallet.sign(message=MESSAGE)
print("Signature:", signature)
print("Verified:", wallet.verify(message=MESSAGE, signature=signature))
