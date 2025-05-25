@echo off
echo Spoustim ZizkaTranscriptTranslate s GPU podporou...
echo.

REM Aktivace virtuálního prostředí
call venv\Scripts\activate.bat

REM Nastavení proměnných prostředí pro optimální výkon
set CUDA_LAUNCH_BLOCKING=0
set TORCH_CUDA_ARCH_LIST=6.0;6.1;7.0;7.5;8.0;8.6;8.9;9.0
set CUDA_VISIBLE_DEVICES=0

REM Přesun do src složky
cd src

REM Spuštění aplikace
python run.py

pause