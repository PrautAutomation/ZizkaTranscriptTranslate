@echo off
echo Testing GPU in Docker...
echo.

docker run --rm --gpus all nvidia/cuda:12.1.0-base-ubuntu22.04 nvidia-smi

echo.
echo Testing PyTorch GPU access...
docker run --rm --gpus all nvidia/cuda:12.1.0-runtime-ubuntu22.04 bash -c "apt-get update && apt-get install -y python3-pip && pip3 install torch && python3 -c 'import torch; print(\"GPU Available:\", torch.cuda.is_available()); print(\"GPU Name:\", torch.cuda.get_device_name(0) if torch.cuda.is_available() else \"None\")'"

pause