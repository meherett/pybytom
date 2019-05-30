# from btmhdw import BTMHDW, BTMHDW_HARDEN, BytomHDWallet
# from unittest import TestCase
#
#
# class UnittestHDWallet(TestCase, BTMHDW):
#
#     def test_generateMnemonic(self):
#
#         enMnemonic = self.generateMnemonic('english')
#
#         enCheck = self.checkMnemonic(enMnemonic, 'english')
#
#         self.assertTrue(enCheck)
#
#         jpMnemonic = self.generateMnemonic('japanese')
#
#         jpCheck = self.checkMnemonic(jpMnemonic, 'japanese')
#
#         self.assertTrue(jpCheck)
#
#     def test_createWallet(self):
#
#         mnemonic = self.generateMnemonic()
#
#         created = self.createWallet(mnemonic=mnemonic,
#                                     passphrase='password')
#
#         self.assertEqual(len(created["xprivate"]), 128)
#
#         self.assertTrue(self.checkMnemonic(created["mnemonic"]))
#
#     def test_walletFromXPrivate(self):
#
#         mnemonic = self.generateMnemonic()
#
#         created = self.createWallet(mnemonic=mnemonic,
#                                     passphrase='password')
#
#         wallet_xprivate = self.walletFromXPrivate(created["xprivate"])
#
#         self.assertEqual(created["address"], wallet_xprivate["address"])
#
#         self.assertEqual(created["xprivate"], wallet_xprivate["xprivate"])
