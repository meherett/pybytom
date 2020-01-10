# from btmhdw import BTMHDW, BTMHDW_HARDEN, BytomHDWallet
# from unittest import TestCase
#
#
# class UnittestHDWallet(TestCase, BTMHDW):
#
#     def test_generateMnemonic(self):
#
#         enMnemonic = self.generate_mnemonic('english')
#
#         enCheck = self.check_mnemonic(enMnemonic, 'english')
#
#         self.assertTrue(enCheck)
#
#         jpMnemonic = self.generate_mnemonic('japanese')
#
#         jpCheck = self.check_mnemonic(jpMnemonic, 'japanese')
#
#         self.assertTrue(jpCheck)
#
#     def test_createWallet(self):
#
#         mnemonic = self.generate_mnemonic()
#
#         created = self.create(mnemonic=mnemonic, passphrase='password')
#
#         self.assertEqual(len(created["xprivate"]), 128)
#
#         self.assertTrue(self.check_mnemonic(created["mnemonic"]))
#
#     def test_walletFromXPrivate(self):
#
#         mnemonic = self.generate_mnemonic()
#
#         created = self.create(mnemonic=mnemonic, passphrase='password')
#
#         wallet_xprivate = self.from_xprivate(created["xprivate"])
#
#         self.assertEqual(created["address"], wallet_xprivate["address"])
#
#         self.assertEqual(created["xprivate"], wallet_xprivate["xprivate"])
