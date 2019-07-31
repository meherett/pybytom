from btmhdw import BTMHDW, BytomHDWallet, BTMHDW_HARDEN, PATH, INDEXES

# MNEMONIC = "ancient young hurt bone shuffle deposit congress normal crack six boost despair"
#
# XPRIVATE = "c003f4bcccf9ad6f05ad2c84fa5ff98430eb8e73de5de232bc29334c7d074759d513bc370335cac" \
#            "51d77f0be5dfe84de024cfee562530b4d873b5f5e2ff4f57c"
#
# XPUBLIC = "3c6664244d2d57168d173c4691dbf8741a67d972b2d3e1b0067eb825e2005d20c5eebd1c26ccad4" \
#           "de5142d7c339bf62cc1fb79a8b3e42a708cd521368dbc9286"
#
# # ####################################### BTMHDW ############################################
#
# # init BTMHDW
# btmhdw = BTMHDW()
#
# # Generate mnemonic english/japanese
# mnemonic = btmhdw.generateMnemonic("japanese")
#
# # Checking mnemonic language
# if not btmhdw.checkMnemonic(mnemonic, "japanese"):
#     exit()
#
# # Create a new wallet
# createdWallet = btmhdw.createWallet(mnemonic=mnemonic, network="mainnet")
#
# print(createdWallet['address'])
# print(createdWallet['xprivate'])
#
# # Wallet from xprivate
# walletFromXPrivate = btmhdw.walletFromXPrivate(xprivate=createdWallet["xprivate"],
#                                                network="mainnet")
# print(walletFromXPrivate['address'])
# print(walletFromXPrivate['xprivate'])
#
# # Checking created address and from xprivate address
# if createdWallet['address'] == walletFromXPrivate['address']:
#     print("Success!")
#
# # ################################### BytomHDWallet ##########################################
#
# # init BytomHDWallet
# bytomHDWallet = BytomHDWallet()
#
# # From mnemonic
# bytomHDWallet = bytomHDWallet.masterKeyFromMnemonic(mnemonic=MNEMONIC)
#
# bytomHDWallet.fromPath("m/44/153/1/0/1")
# # or
# # bytomHDWallet.fromIndex(44)
# # bytomHDWallet.fromIndex(153)
# # bytomHDWallet.fromIndex(1)  # account
# # bytomHDWallet.fromIndex(0)  # change 0 or 1
# # bytomHDWallet.fromIndex(1)  # address
#
# # Getting path indexes array
# print(bytomHDWallet.getIndexes())
# # Getting XPrivate key of MNEMONIC
# print(bytomHDWallet.xprivateKey())
# # Getting XPublic key of MNEMONIC
# print(bytomHDWallet.xpublicKey())
# # Getting Expand private key from XPrivate key of MNEMONIC
# print(bytomHDWallet.expandPrivateKey())
# # Getting Public key length 64 of MNEMONIC
# print(bytomHDWallet.publicKey())
# # Getting contract program of MNEMONIC
# print(bytomHDWallet.program())
# # Getting Address of MNEMONIC
# print(bytomHDWallet.address())
# # Getting seed of MNEMONIC
# print(bytomHDWallet.seed.hex())
#
# # ################################### BytomHDWallet() ##########################################
#
# # Getting contract Program from xpublic and path or indexes
# print(BytomHDWallet().program(xpublic=XPUBLIC, path="m/44/153/2/0/8"))
# print(BytomHDWallet().program(xpublic=XPUBLIC, path=PATH))
# print(BytomHDWallet().program(xpublic=XPUBLIC, indexes=INDEXES))
# print(BytomHDWallet().program(xpublic=XPUBLIC, indexes=['2c000000', '99000000', '01000000', '01000000', '01000000']))
#
# program = BytomHDWallet().program(xpublic=XPUBLIC, path=PATH)
# print(bytomHDWallet.address(program=program,
#                             network='mainnet'))  # or network bm
# print(bytomHDWallet.address(program=program,
#                             network='testnet'))  # or network tm
# print(bytomHDWallet.address(program=program,
#                             network='solonet'))  # or network sm
#
# # ################################### BytomHDWallet ##########################################
#
# # init BytomHDWallet
# bytomHDWallet = BytomHDWallet()
#
# # Automatically mnemonic generate by password "meherett"
# bytomHDWallet, mnemonic = bytomHDWallet\
#     .masterKeyFromEntropy(passphrase="meherett",
#                           language="japanese")
#
# # bytomHDWallet.fromPath("m/44/153/1/0/1")
# # or
# bytomHDWallet.fromIndex(44)
# bytomHDWallet.fromIndex(153)
# bytomHDWallet.fromIndex(1)  # account
# bytomHDWallet.fromIndex(0)  # change 0 or 1
# bytomHDWallet.fromIndex(1)  # address
# # Advanced BTMHDW_HARDEN
# # bytomHDWallet.fromIndex(44 + BTMHDW_HARDEN)
# # bytomHDWallet.fromIndex(153)
# # bytomHDWallet.fromIndex(1 + BTMHDW_HARDEN)
# # bytomHDWallet.fromIndex(0)
# # bytomHDWallet.fromIndex(1)
#
# # Getting entropy
# print(bytomHDWallet.entropy.hex())
# # Getting entropy
# print(mnemonic)
# # Getting path indexes array
# print(bytomHDWallet.getIndexes())
# # Getting XPrivate key
# print(bytomHDWallet.xprivateKey())
# # Getting XPublic key
# print(bytomHDWallet.xpublicKey())
# # Getting Expand private key from XPrivate key
# print(bytomHDWallet.expandPrivateKey())
# # Getting Public key length 64
# print(bytomHDWallet.publicKey())
# # Getting contract program
# print(bytomHDWallet.program())
# # Getting Address
# print(bytomHDWallet.address())
# # Getting seed
# print(bytomHDWallet.seed.hex())

pv = "e8d474e7d265c9c02ed4f0352f8ec53ca5e79b869df4fe79d9644e5d940c1f4576412d0824fcb38f0141733334ae671aed902c23242a34a2dbe64a90b02527d0"
pu = "e8a63461c2e898d28ff10b50a03d5ee6e1a77088bd0b84a60682816945f685be76412d0824fcb38f0141733334ae671aed902c23242a34a2dbe64a90b02527d0"
path = "m/44/153/1/0/1"
network = "mainnet"

vp = BTMHDW().walletFromXPrivate(xprivate=pv, path=path, network=network)

program = BytomHDWallet().program(xpublic=pu, path=path)

print(vp['program'])
print(program)

address = BytomHDWallet().address(program=program, network=network)

print(vp['address'])
print(address)
