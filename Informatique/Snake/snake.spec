# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['snake.py'],
    pathex=[],
    binaries=[],
    datas=[('C:\\GitHub2\\Informatique\\Snake\\musique_fond.mp3', '.'), ('C:\\GitHub2\\Informatique\\Snake\\game_over.wav', '.'), ('C:\\GitHub2\\Informatique\\Snake\\PressStart2P.ttf', '.')],
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
    name='snake',
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
    icon=['C:\\GitHub2\\Informatique\\Snake\\mon_icone.ico'],
)
