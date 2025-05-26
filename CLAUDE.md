# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Czech web application that transcribes audio to text using OpenAI's Whisper model and translates the results. It's built with FastAPI and provides a web interface for uploading audio files and downloading subtitle files (SRT/VTT format) with translations.

## Architecture

- **FastAPI Backend** (`src/main.py`): Core application with audio processing, transcription, and translation endpoints
- **Web Interface** (`src/templates/index.html`): Single-page form for file upload and configuration
- **Static Assets** (`src/static/`): CSS, JavaScript, and logo images including animated logo sequence
- **Entry Point** (`src/run.py`): Development server launcher that opens browser and starts uvicorn

## Key Dependencies

- `stable-ts`: Enhanced Whisper implementation for better timestamp accuracy
- `deep_translator`: Google Translate integration for multilingual support
- `ffmpeg-python`: Audio file processing and format conversion
- `fastapi` + `uvicorn`: Web framework and ASGI server

## Development Commands

### Local Development
```bash
# Setup virtual environment
python3 -m venv venv
source venv/bin/activate  # or `. venv/bin/activate`

# Install dependencies
pip install -r requirements.txt

# Run development server (from src/ directory)
cd src
python3 run.py
# Opens browser to http://127.0.0.1:18666/
```

### Docker Development
```bash
# Build CPU image
docker build -t appold .

# Build GPU image (requires NVIDIA Docker)
docker build -f Dockerfile.gpu -t appold-gpu .

# Run CPU container
docker run --name app_container -p 18666:18666 appold

# Run GPU container (requires NVIDIA Docker runtime)
docker run --gpus all --name app_container_gpu -p 18666:18666 appold-gpu

# Restart existing container
docker start app_container
```

### Production Deployment
Uses docker-compose with external proxy network for domain hosting at zizka.praut.cz

## Core Functionality

1. **Audio Upload**: Accepts various audio formats via web form
2. **Whisper Transcription**: Processes audio using configurable model sizes (tiny to large)
3. **Translation**: Translates transcribed text to target language using Google Translate
4. **Subtitle Generation**: Creates SRT/VTT files with configurable character limits and timestamp splitting
5. **File Download**: Streams generated subtitle files back to user

## File Processing Flow

1. Audio file saved as `audio.mp3`
2. Whisper model loads and transcribes with timestamp segments
3. Text chunks split by punctuation respecting character limits
4. Translation applied per segment
5. SRT/VTT file generated with proper timing distribution
6. File streamed as download response