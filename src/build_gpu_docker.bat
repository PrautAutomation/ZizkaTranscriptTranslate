@echo off
echo ===============================================
echo Building GPU Docker image...
echo ===============================================

docker build -f Dockerfile.gpu -t zizka-whisper-gpu .

echo.
echo Build completed!
pause