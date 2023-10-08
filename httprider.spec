# -*- mode: python -*-

block_cipher = None

import httprider

a = Analysis(['bin/app'],
             pathex=['.'],
             binaries=None,
             datas=[
                ('resources/images/*', 'resources/images'),
                ('resources/icons/*', 'resources/icons'),
                ('resources/fonts/*', 'resources/fonts'),
                ('resources/themes/*', 'resources/themes'),
             ],
             hiddenimports=[],
             hookspath=None,
             runtime_hooks=None,
             excludes=None,
             cipher=block_cipher)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(pyz,
          a.scripts,
          exclude_binaries=True,
          name='app',
          debug=False,
          strip=False,
          upx=True,
          console=False,
          icon='resources\\icons\\httprider.ico')

coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               name='HttpRider')

app = BUNDLE(coll,
             name='{}.app'.format(httprider.__appname__),
             icon='resources/icons/httprider.icns',
             bundle_identifier=None,
             info_plist={
                'CFBundleShortVersionString': httprider.__version__,
                'NSHighResolutionCapable': 'True'
                }
             )
