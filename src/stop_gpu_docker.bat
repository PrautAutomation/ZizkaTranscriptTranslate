@echo off
echo Stopping GPU Docker container...
docker-compose -f docker-compose-gpu.yml down
pause