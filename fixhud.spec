# -*- mode: python -*-
a = Analysis(['fixhud.py'],
             pathex=['/srv/http/lol-eyefinity-surround-lazy-hudfixer'],
             hiddenimports=[],
             hookspath=None,
             runtime_hooks=None)
pyz = PYZ(a.pure)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='fixhud',
          debug=False,
          strip=None,
          upx=True,
          console=True )
