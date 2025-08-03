# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['C:\\Github\\inventory-management-desktop\\inv_app.py'],
    pathex=[],
    binaries=[],
    datas=[('png', 'png'), ('db', 'db')],
    hiddenimports=['flet', 'flet_desktop', 'sqlite3', 'asyncio'],
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
    name='InventoryManagementSystem',
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
    icon=['png\\Blue Black Minimalist Solar Panel Logo.png'],
)
