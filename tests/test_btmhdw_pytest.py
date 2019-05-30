from btmhdw import BTMHDW, BTMHDW_HARDEN, BytomHDWallet

btmhdw = BTMHDW()


def test_generateMnemonic():

    enMnemonic = btmhdw.generateMnemonic('english')

    enCheck = btmhdw.checkMnemonic(enMnemonic, 'english')

    assert enCheck

    jpMnemonic = btmhdw.generateMnemonic('japanese')

    jpCheck = btmhdw.checkMnemonic(jpMnemonic, 'japanese')

    assert jpCheck


def test_createWallet():

    mnemonic = btmhdw.generateMnemonic()

    created = btmhdw.createWallet(mnemonic=mnemonic,
                                  passphrase='password')

    assert len(created["xprivate"]) == 128

    assert btmhdw.checkMnemonic(created["mnemonic"])


def test_walletFromXPrivate():

    mnemonic = btmhdw.generateMnemonic()

    created = btmhdw.createWallet(mnemonic=mnemonic,
                                  passphrase='password')

    wallet_xprivate = btmhdw.walletFromXPrivate(created["xprivate"])

    assert created["address"] == wallet_xprivate["address"]

    assert created["xprivate"] == wallet_xprivate["xprivate"]
