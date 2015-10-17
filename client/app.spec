# -*- mode: python -*-
a = Analysis(['app.py'],
             pathex=['/Users/sdiemert/workspace/actua/clicker/client'],
             hiddenimports=[],
             hookspath=None,
             runtime_hooks=None)
pyz = PYZ(a.pure)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='app',
          debug=False,
          strip=None,
          upx=True,
          console=False )
app = BUNDLE(exe,
             name='app.app',
             icon=None)
