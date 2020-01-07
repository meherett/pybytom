from btmhdw import BTMHDW, BytomHDWallet, BTMHDW_HARDEN, PATH, INDEXES, sign, verify

MNEMONIC = "ancient young hurt bone shuffle deposit congress normal crack six boost despair"

XPRIVATE = "c003f4bcccf9ad6f05ad2c84fa5ff98430eb8e73de5de232bc29334c7d074759d513bc370335cac" \
           "51d77f0be5dfe84de024cfee562530b4d873b5f5e2ff4f57c"

XPUBLIC = "3c6664244d2d57168d173c4691dbf8741a67d972b2d3e1b0067eb825e2005d20c5eebd1c26ccad4" \
          "de5142d7c339bf62cc1fb79a8b3e42a708cd521368dbc9286"

MESSAGE = "27c42b40a7a35a6d489fb2e41bde15bdb4b4c276045bd0628525b88c2abbc4c0"

# ####################################### BTMHDW ############################################

# init BTMHDW
btmhdw = BTMHDW()

# Generate mnemonic english/japanese
mnemonic = btmhdw.generate_mnemonic("japanese")

# # Checking mnemonic language
# if not btmhdw.check_mnemonic(mnemonic, "japanese"):
#     exit()

# Create a new wallet
wallet = btmhdw.create(mnemonic=MNEMONIC, network="mainnet")

print(wallet['address'])
print(wallet['xprivate'])

# Wallet from xprivate
wallet_from_xprivate = btmhdw.wallet_from_xprivate(xprivate=wallet["xprivate"],
                                                   network="mainnet")
print(wallet_from_xprivate['address'])
print(wallet_from_xprivate['xprivate'])

# Checking created address and from xprivate address
if wallet['address'] == wallet_from_xprivate['address']:
    print("Success!")

# ################################### Sing and VerifyMessage ##########################################

signature = sign(xprivate=wallet['xprivate'], message=MESSAGE)
print("Signature", signature)
print("Signature Verify", verify(xpublic=wallet['xpublic'], signature=signature, message=MESSAGE))

# ################################### BytomHDWallet ##########################################

# init BytomHDWallet
bytomHDWallet = BytomHDWallet()

# From mnemonic
bytomHDWallet = bytomHDWallet.master_key_from_mnemonic(mnemonic=MNEMONIC)

bytomHDWallet.from_path("m/44/153/1/0/1")
# or
# bytomHDWallet.from_index(44)
# bytomHDWallet.from_index(153)
# bytomHDWallet.from_index(1)  # account
# bytomHDWallet.from_index(0)  # change 0 or 1
# bytomHDWallet.from_index(1)  # address

# Getting path indexes array
print(bytomHDWallet.get_indexes())
# Getting XPrivate key of MNEMONIC
print("prv", bytomHDWallet.xprivate_key())
# Getting XPublic key of MNEMONIC
print("pub", bytomHDWallet.xpublic_key())
# Getting Expand private key from XPrivate key of MNEMONIC
print(bytomHDWallet.expand_xprivate_key())
# Getting Public key length 64 of MNEMONIC
print(bytomHDWallet.public_key())
# Getting contract program of MNEMONIC
print(bytomHDWallet.program())
# Getting Address of MNEMONIC
print(bytomHDWallet.address())
# Getting seed of MNEMONIC
print(bytomHDWallet.seed.hex())

print("Signing and Verifying")
# Signing messages
print(bytomHDWallet.sign(message=MESSAGE))
# Verifying messages
print(bytomHDWallet.verify(message=MESSAGE,
                           signature=bytomHDWallet.sign(message=MESSAGE)))

# ################################### BytomHDWallet() ##########################################

# Getting contract Program from xpublic and path or indexes
print(BytomHDWallet().program(xpublic=XPUBLIC, path="m/44/153/2/0/8"))
print(BytomHDWallet().program(xpublic=XPUBLIC, path=PATH))
print(BytomHDWallet().program(xpublic=XPUBLIC, indexes=INDEXES))
print(BytomHDWallet().program(xpublic=XPUBLIC, indexes=['2c000000', '99000000', '01000000', '01000000', '01000000']))

program = BytomHDWallet().program(xpublic=XPUBLIC, path=PATH)
print(bytomHDWallet.address(program=program,
                            network='mainnet'))  # or network bm
print(bytomHDWallet.address(program=program,
                            network='testnet'))  # or network tm
print(bytomHDWallet.address(program=program,
                            network='solonet'))  # or network sm

# ################################### BytomHDWallet ##########################################

# init BytomHDWallet
bytomHDWallet = BytomHDWallet()

# Automatically mnemonic generate by password "meherett"
bytomHDWallet, mnemonic = bytomHDWallet\
    .master_key_from_entropy(passphrase="meherett",
                             language="japanese")

# bytomHDWallet.from_path("m/44/153/1/0/1")
# or
bytomHDWallet.from_index(44)
bytomHDWallet.from_index(153)
bytomHDWallet.from_index(1)  # account
bytomHDWallet.from_index(0)  # change 0 or 1
bytomHDWallet.from_index(1)  # address
# Advanced BTMHDW_HARDEN
# bytomHDWallet.from_index(44 + BTMHDW_HARDEN)
# bytomHDWallet.from_index(153)
# bytomHDWallet.from_index(1 + BTMHDW_HARDEN)
# bytomHDWallet.from_index(0)
# bytomHDWallet.from_index(1)

# Getting entropy
print(bytomHDWallet.entropy.hex())
# Getting entropy
print(mnemonic)
# Getting path indexes array
print(bytomHDWallet.get_indexes())
# Getting XPrivate key
print(bytomHDWallet.xprivate_key())
# Getting XPublic key
print(bytomHDWallet.xpublic_key())
# Getting Expand private key from XPrivate key
print(bytomHDWallet.expand_xprivate_key())
# Getting Public key length 64
print(bytomHDWallet.public_key())
# Getting contract program
print(bytomHDWallet.program())
# Getting Address
print(bytomHDWallet.address())
# Getting seed
print(bytomHDWallet.seed.hex())
