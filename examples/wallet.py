#!/usr/bin/env python3

from bytom.wallet import Wallet, PATH, INDEXES

MNEMONIC = "indicate warm sock mistake code spot acid ribbon sing over taxi toast"

MESSAGE = "a0841d35364046649ab8fc4af5a6266245890778f6cf7304696c4ab8edd86242"

wallet = Wallet(network="mainnet")\
    .from_mnemonic(mnemonic=MNEMONIC)

# wallet.from_path(path=PATH)
# or
# wallet.from_indexes(indexes=INDEXES)

# Custom path
# wallet.from_path("m/44/153/1/0/1")
# or index
wallet.from_index(44)
wallet.from_index(153)
wallet.from_index(1)  # account
wallet.from_index(0)  # change false(0) or true(1)
wallet.from_index(1)  # address

print("Entropy:", wallet.entropy())
print("Mnemonic:", wallet.mnemonic())
print("XPrivate Key:", wallet.xprivate_key())
print("Expand XPrivate Key:", wallet.expand_xprivate_key())
print("XPublic Key:", wallet.xpublic_key())
print("Seed:", wallet.seed())
print("Indexes:", wallet.indexes())
print("Private Key:", wallet.private_key())
print("Public Key:", wallet.public_key())
print("Program:", wallet.program())
print("Address:", wallet.address())
print("Path:", wallet.path())

print("Message:", MESSAGE)
print("Sign:", wallet.sign(message=MESSAGE))
print("Verify:", wallet.verify(message=MESSAGE,
                               signature=wallet.sign(message=MESSAGE)))
