# -- coding: utf-8 --

import sys
from PyInstaller import __main__

# Tente corrigir a estrutura do seu arquivo .spec para que ele fique assim:

a = Analysis(
    ['Projeto 06.py'],
    pathex=['C:\\Users\\user\\documents\\projetos\\Laquae\\projeto4'],
    binaries=[],
    datas=[],
    hiddenimports=[],
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher_code=None,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='Projeto 06',
    debug=False,
    strip=False,
    upx=True,
    console=True
)

