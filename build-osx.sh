#!/bin/sh
rm -Rf build/
rm -Rf dist/
pyinstaller --onefile --windowed --clean --noconfirm --icon=fixhud.icns fixhud.py