#!/bin/sh
IF EXIST "build/" (
    rmdir "build/" /s /q
)

IF EXIST "dist/" (
    rmdir "dist/" /s /q
)

pyinstaller --onefile --windowed --clean --noconfirm --icon=fixhud.ico fixhud.py