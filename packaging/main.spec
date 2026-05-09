# -*- mode: python ; coding: utf-8 -*-

from pathlib import Path

SPEC_DIR = Path(SPECPATH)
if SPEC_DIR.suffix == '.spec':
    SPEC_DIR = SPEC_DIR.parent
ROOT_DIR = SPEC_DIR.parent if SPEC_DIR.name == 'packaging' else SPEC_DIR


a = Analysis(
    [str(ROOT_DIR / 'src' / 'main.py')],
    pathex=[str(ROOT_DIR / 'src')],
    binaries=[],
    datas=[(str(ROOT_DIR / 'assets'), 'assets')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='main',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=[str(ROOT_DIR / 'assets' / 'images' / 'icon.ico')],
)