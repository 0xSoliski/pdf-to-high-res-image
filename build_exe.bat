@echo off
echo Building PDF to Image Converter executable...
echo.

REM Check if pyinstaller is installed
python -m PyInstaller --version >nul 2>&1
if errorlevel 1 (
    echo PyInstaller not found. Installing...
    pip install pyinstaller
    echo.
)

REM Build the executable (optimized for Windows; strip removed to avoid missing strip.exe)
echo Building executable with PyInstaller (optimized)...
pyinstaller --onefile --console --optimize=2 --clean --noupx pdf_to_image.py

echo.
echo Build complete!
echo Executable can be found in: dist\pdf_to_image.exe
echo.
pause
pause
