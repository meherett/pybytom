from btmhdw import BTMHDW, BytomHDWallet, BTMHDW_HARDEN, PATH, INDEXES

import hashlib

MNEMONIC = "ancient young hurt bone shuffle deposit congress normal crack six boost despair"

XPRIVATE = "c003f4bcccf9ad6f05ad2c84fa5ff98430eb8e73de5de232bc29334c7d074759d513bc370335cac" \
           "51d77f0be5dfe84de024cfee562530b4d873b5f5e2ff4f57c"

XPUBLIC = "3c6664244d2d57168d173c4691dbf8741a67d972b2d3e1b0067eb825e2005d20c5eebd1c26ccad4" \
          "de5142d7c339bf62cc1fb79a8b3e42a708cd521368dbc9286"

btmhdw = BTMHDW()


def test_generateMnemonic():

    enMnemonic = btmhdw.generate_mnemonic('english')

    enCheck = btmhdw.check_mnemonic(enMnemonic, 'english')

    assert enCheck

    jpMnemonic = btmhdw.generate_mnemonic('japanese')

    jpCheck = btmhdw.check_mnemonic(jpMnemonic, 'japanese')

    assert jpCheck


def test_createWallet():

    mnemonic = btmhdw.generate_mnemonic()

    created = btmhdw.create(mnemonic=mnemonic, passphrase='password')

    assert len(created["xprivate"]) == 128

    assert btmhdw.check_mnemonic(created["mnemonic"])


def test_walletFromXPrivate():

    mnemonic = btmhdw.generate_mnemonic()

    created = btmhdw.create(mnemonic=mnemonic, passphrase='password')

    wallet_xprivate = btmhdw.wallet_from_xprivate(created["xprivate"])

    assert created["address"] == wallet_xprivate["address"]

    assert created["xprivate"] == wallet_xprivate["xprivate"]


def test_masterKeyFromMnemonic():
    bytomHDWallet = BytomHDWallet().master_key_from_mnemonic(mnemonic=MNEMONIC)

    bytomHDWallet.from_path("m/44/153/1/0/1")
    assert (bytomHDWallet.program())
    assert (bytomHDWallet.address(network="testnet"))
    assert (bytomHDWallet.seed.hex())


def test_BytomHDWallet_Functions():
    assert (BytomHDWallet().program(xpublic=XPUBLIC, path="m/44/153/2/0/8"))
    assert (BytomHDWallet().program(xpublic=XPUBLIC, path=PATH))
    assert (BytomHDWallet().program(xpublic=XPUBLIC, indexes=INDEXES))
    assert (BytomHDWallet().program(xpublic=XPUBLIC,
                                    indexes=['2c000000', '99000000', '01000000', '01000000', '01000000']))
    bytomHDWallet = BytomHDWallet()
    program = BytomHDWallet().program(xpublic=XPUBLIC, path=PATH)
    assert (bytomHDWallet.address(program=program,
                                  network='mainnet'))  # or network bm
    assert (bytomHDWallet.address(program=program,
                                  network='testnet'))  # or network tm
    assert (bytomHDWallet.address(program=program,
                                  network='solonet'))  # or network sm


def test_HARDEN():
    bytomHDWallet = BytomHDWallet()

    bytomHDWallet, mnemonic = bytomHDWallet\
        .master_key_from_entropy(passphrase="meherett", language="japanese")

    bytomHDWallet.from_index(44 + BTMHDW_HARDEN)
    bytomHDWallet.from_index(153)
    bytomHDWallet.from_index(1 + BTMHDW_HARDEN)
    bytomHDWallet.from_index(0)
    bytomHDWallet.from_index(1)
    assert (bytomHDWallet.program())
    assert (bytomHDWallet.address(network="testnet"))


def test_sing_and_verify():
    bytomHDWallet = BytomHDWallet()

    bytomHDWallet, mnemonic = bytomHDWallet \
        .master_key_from_entropy(passphrase="meherett", language="japanese")

    bytomHDWallet.from_index(44 + BTMHDW_HARDEN)
    bytomHDWallet.from_index(153)
    bytomHDWallet.from_index(1 + BTMHDW_HARDEN)
    bytomHDWallet.from_index(0)
    bytomHDWallet.from_index(1)

    signature = bytomHDWallet.sign(message=hashlib.sha256("meherett".encode()).hexdigest())
    assert signature

    assert bytomHDWallet.verify(message=hashlib.sha256("meherett".encode()).hexdigest(),
                                signature=signature)
