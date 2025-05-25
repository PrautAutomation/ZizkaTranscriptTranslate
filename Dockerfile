FROM nvidia/cuda:12.1.0-cudnn8-runtime-ubuntu22.04

# Nastavení prostředí
ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONUNBUFFERED=1
ENV CUDA_VISIBLE_DEVICES=0
ENV TORCH_CUDA_ARCH_LIST="6.0;6.1;7.0;7.5;8.0;8.6;8.9;9.0"

# Instalace systémových závislostí
RUN apt-get update && apt-get install -y \
    python3.10 \
    python3-pip \
    python3.10-dev \
    ffmpeg \
    git \
    wget \
    && rm -rf /var/lib/apt/lists/*

# Vytvoření symbolického odkazu pro python
RUN ln -s /usr/bin/python3.10 /usr/bin/python

WORKDIR /appold

# Instalace PyTorch s CUDA podporou
RUN pip3 install --no-cache-dir torch==2.1.0+cu121 torchaudio==2.1.0+cu121 --index-url https://download.pytorch.org/whl/cu121

# Kopírování requirements a instalace
COPY requirements.txt /appold/
RUN pip3 install --no-cache-dir -r requirements.txt

# Kopírování aplikace
COPY src/ /appold/

# Vytvoření složky pro modely
RUN mkdir -p /appold/models

# Předstažení modelu turbo
RUN python -c "import stable_whisper; stable_whisper.load_model('turbo', device='cpu', download_root='/appold/models')"

# Port
EXPOSE 18666

# Spuštění aplikace
CMD ["python", "-m", "uvicorn", "main:appold", "--host", "0.0.0.0", "--port", "18666"]