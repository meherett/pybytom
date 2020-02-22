#!/usr/bin/env python3

from bytom import Wallet, PATH, INDEXES

MNEMONIC = "indicate warm sock mistake code spot acid ribbon sing over taxi toast"

MESSAGE = "1246b84985e1ab5f83f4ec2bdf271114666fd3d9e24d12981a3c861b9ed523c6"

wallet = Wallet(network="mainnet")\
    .from_mnemonic(mnemonic=MNEMONIC)

# wallet.from_path(path=PATH)
# or
# wallet.from_indexes(indexes=INDEXES)

# Custom path
wallet.from_path("m/44/153/1/0/1")
# or index
# wallet.from_index(44)
# wallet.from_index(153)
# wallet.from_index(1)  # account
# wallet.from_index(0)  # change false(0) or true(1)
# wallet.from_index(1)  # address

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
