@echo off
echo ===============================================
echo Starting ZizkaTranscriptTranslate GPU Container
echo ===============================================

REM Kontrola GPU v Docker
docker run --rm --gpus all nvidia/cuda:12.1.0-base-ubuntu22.04 nvidia-smi

echo.
echo Starting application container...
docker-compose -f docker-compose-gpu.yml up -d

echo.
echo ===============================================
echo Application is running at: http://localhost:18666
echo ===============================================
echo.
echo To view logs: docker-compose -f docker-compose-gpu.yml logs -f
echo To stop: docker-compose -f docker-compose-gpu.yml down
echo.
pause