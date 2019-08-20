# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

datas = [
     ('/root/PycharmProjects/btmhdw/gui/BTMHDW.ico', '.'),
     ('/root/PycharmProjects/btmhdw/gui/BTMHDW.png', '.'),
     ('/root/PycharmProjects/btmhdw/gui/BTMHDW.svg', '.'),
     ('/root/PycharmProjects/btmhdw/gui/icons/checkbox_checked.svg', 'icons'),
     ('/root/PycharmProjects/btmhdw/gui/icons/checkbox_unchecked.svg', 'icons'),
     ('/root/PycharmProjects/btmhdw/gui/icons/radio_checked.svg', 'icons'),
     ('/root/PycharmProjects/btmhdw/gui/icons/radio_unchecked.svg', 'icons'),
     ('/root/.pyenv/versions/3.7.4/lib/python3.7/site-packages/mnemonic/wordlist/english.txt', 'mnemonic/wordlist'),
     ('/root/.pyenv/versions/3.7.4/lib/python3.7/site-packages/mnemonic/wordlist/japanese.txt', 'mnemonic/wordlist')
]

a = Analysis(['BTMHDW.py'],
             pathex=['/root/PycharmProjects/btmhdw/gui'],
             binaries=[],
             datas=datas,
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='BTMHDW',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          icon='/root/PycharmProjects/btmhdw/gui/BTMHDW.ico',
          upx_exclude=[],
          runtime_tmpdir=None,
          console=False )
