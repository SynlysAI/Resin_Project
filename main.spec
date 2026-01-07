# -*- mode: python ; coding: utf-8 -*-


import os
import sys

a = Analysis(
    ['main.py'],
    pathex=[os.getcwd()],
    binaries=[
        ('Drivers\\EthernetDevices\\zmcdll\\zauxdll.dll', 'zmcdll'),
        ('Drivers\\EthernetDevices\\zmcdll\\zmotion.dll', 'zmcdll'),
        ('Drivers\\EthernetDevices\\zmcdll\\mfc100.dll', 'zmcdll'),
        ('Drivers\\EthernetDevices\\zmcdll\\mfc140.dll', 'zmcdll'),
        ('Drivers\\EthernetDevices\\zmcdll\\msvcp100.dll', 'zmcdll'),
        ('Drivers\\EthernetDevices\\zmcdll\\msvcp120.dll', 'zmcdll'),
        ('Drivers\\EthernetDevices\\zmcdll\\msvcp140.dll', 'zmcdll'),
        ('Drivers\\EthernetDevices\\zmcdll\\msvcr100.dll', 'zmcdll'),
        ('Drivers\\EthernetDevices\\zmcdll\\msvcr120.dll', 'zmcdll'),
    ],
    datas=[
        ('Drivers\\EthernetDevices\\zmcdll\\zauxdllPython.py', 'zmcdll'),
        ('Drivers\\EthernetDevices\\zmcdll\\__init__.py', 'zmcdll'),
    ],
    hiddenimports=[
        'Drivers.EthernetDevices.ZMC',
        'Drivers.EthernetDevices.MotorZmc',
        'Drivers.EthernetDevices.SRND_16_IO',
        'Drivers.SerialDevices.TemperatureController',
        'Drivers.SerialDevices.tools.hex_utils',
        'Drivers.EthernetDevices.tools.modbus_rtu_over_tcp_labware',
        'zmcdll.zauxdllPython',
        'Drivers.EthernetDevices.inovance_three_axis.tools.modbus',
        'Drivers.EthernetDevices.inovance_three_axis.tools.client',
    ],
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
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
