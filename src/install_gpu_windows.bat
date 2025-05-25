@echo off
echo ===============================================
echo Instalace GPU verze ZizkaTranscriptTranslate
echo ===============================================
echo.

REM Kontrola Python verze
py --version >nul 2>&1
if %errorlevel% neq 0 (
    echo CHYBA: Python neni nainstalovan!
    echo Nainstalujte Python 3.9 nebo novejsi z https://www.python.org/
    pause
    exit /b 1
)

REM Vytvoření virtuálního prostředí
echo Vytvarim virtualni prostredi...
py -m venv venv

REM Aktivace virtuálního prostředí
echo Aktivuji virtualni prostredi...
call venv\Scripts\activate.bat

REM Upgrade pip
echo Aktualizuji pip...
py -m pip install --upgrade pip

REM Instalace PyTorch s CUDA podporou
echo.
echo Instaluji PyTorch s GPU podporou...
py -m pip install torch==2.1.0+cu121 torchaudio==2.1.0+cu121 --index-url https://download.pytorch.org/whl/cu121

REM Instalace ostatních závislostí
echo.
echo Instaluji ostatni zavislosti...
py -m pip install -r requirements.txt

REM Vytvoření složky pro modely
echo.
echo Vytvarim slozku pro modely...
if not exist "src\models" mkdir "src\models"

REM Kontrola GPU
echo.
echo Kontroluji GPU...
py -c "import torch; print('GPU dostupna:', torch.cuda.is_available()); print('GPU:', torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'Zadna')"

echo.
echo ===============================================
echo Instalace dokoncena!
echo.
echo Pro spusteni aplikace pouzijte: run_gpu.bat
echo ===============================================
pause