# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

datas = [
     ('C:/Users/Admin/PycharmProjects/btmhdw/gui/BTMHDW.ico', '.'),
     ('C:/Users/Admin/PycharmProjects/btmhdw/gui/BTMHDW.png', '.'),
     ('C:/Users/Admin/PycharmProjects/btmhdw/gui/BTMHDW.svg', '.'),
     ('C:/Users/Admin/PycharmProjects/btmhdw/gui/BTMHDW-LIGHT.qss', '.'),
     ('C:/Users/Admin/PycharmProjects/btmhdw/gui/icons/checkbox_checked.svg', 'icons'),
     ('C:/Users/Admin/PycharmProjects/btmhdw/gui/icons/checkbox_unchecked.svg', 'icons'),
     ('C:/Users/Admin/PycharmProjects/btmhdw/gui/icons/radio_checked.svg', 'icons'),
     ('C:/Users/Admin/PycharmProjects/btmhdw/gui/icons/radio_unchecked.svg', 'icons'),
     ('C:/Users/Admin/AppData/Local/Programs/Python/Python37-32/Lib/site-packages/mnemonic/wordlist/english.txt', 'mnemonic/wordlist'),
     ('C:/Users/Admin/AppData/Local/Programs/Python/Python37-32/Lib/site-packages/mnemonic/wordlist/japanese.txt', 'mnemonic/wordlist')
]

a = Analysis(['BTMHDW.py'],
             pathex=['C:/Users/Admin/PycharmProjects/btmhdw/gui'],
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
          icon='C:/Users/Admin/PycharmProjects/btmhdw/gui/BTMHDW.ico',
          upx_exclude=[],
          runtime_tmpdir=None,
          console=False )
