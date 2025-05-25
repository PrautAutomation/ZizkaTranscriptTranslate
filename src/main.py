from datetime import timedelta
from typing import Optional
import os
import torch
import logging

from fastapi import FastAPI, Request, File, Form
from fastapi.responses import HTMLResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import ffmpeg
import numpy as np
import srt as srt
import stable_whisper
from deep_translator import GoogleTranslator

# Nastavení loggingu
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# GPU konfigurace
if torch.cuda.is_available():
    torch.cuda.empty_cache()
    # Nastavení pro optimální výkon
    torch.backends.cudnn.benchmark = True
    torch.backends.cuda.matmul.allow_tf32 = True
    device = "cuda"
    logger.info(f"GPU detekována: {torch.cuda.get_device_name(0)}")
    logger.info(f"Dostupná paměť GPU: {torch.cuda.get_device_properties(0).total_memory / 1024**3:.2f} GB")
else:
    device = "cpu"
    logger.warning("GPU není dostupná, používám CPU")

DEFAULT_MAX_CHARACTERS = 80

# Cache pro modely
model_cache = {}

def get_model(model_type: str):
    """Získá model z cache nebo načte nový"""
    if model_type not in model_cache:
        logger.info(f"Načítám model {model_type} na {device}")
        model_cache[model_type] = stable_whisper.load_model(
            model_type, 
            device=device,
            compute_type="float16" if device == "cuda" else "float32",
            download_root="./models"  # Lokální cache modelů
        )
    return model_cache[model_type]

def get_audio_buffer(filename: str, start: int, length: int):
    """
    input: filename of the audio file, start time in seconds, length of the audio in seconds
    output: np array of the audio data which the model's transcribe function can take as input
    """
    out, _ = (
        ffmpeg.input(filename, threads=0)
        .output("-", format="s16le", acodec="pcm_s16le", ac=1, ar=16000, ss=start, t=length)
        .run(cmd=["ffmpeg", "-nostdin"], capture_stdout=True, capture_stderr=True)
    )

    return np.frombuffer(out, np.int16).flatten().astype(np.float32) / 32768.0


def transcribe_time_stamps(segments: list):
    """
    input: a list of segments from the model's transcribe function
    output: a string of the timestamps and the text of each segment
    """
    string = ""
    for seg in segments:
        string += " ".join([str(seg.start), "->", str(seg.end), ": ", seg.text.strip(), "\n"])
    return string


def split_text_by_punctuation(text: str, max_length: int):
    chunks = []
    while len(text) > max_length:
        split_pos = max(
            (text.rfind(p, 0, max_length) for p in [",", ".", "?", "!"," "] if p in text[:max_length]),
            default=-1
        )

        if split_pos == -1:
            split_pos = max_length

        chunks.append(text[:split_pos + 1].strip())
        text = text[split_pos + 1:].strip()

    if text:
        chunks.append(text)

    return chunks


def translate_text(text: str, translate_to: str):
    try:
        return GoogleTranslator(source='auto', target=translate_to).translate(text=text)
    except Exception as e:
        logger.error(f"Chyba při překladu: {e}")
        return text


def make_srt_subtitles(segments: list, translate_to: str, max_chars: int):
    subtitles = []
    for i, seg in enumerate(segments, start=1):
        start_time = seg.start
        end_time = seg.end
        text = translate_text(seg.text.strip(), translate_to)

        text_chunks = split_text_by_punctuation(text, max_chars)
        duration = (end_time - start_time) / len(text_chunks)

        for j, chunk in enumerate(text_chunks):
            chunk_start = start_time + j * duration
            chunk_end = chunk_start + duration

            subtitle = srt.Subtitle(
                index=len(subtitles) + 1,
                start=timedelta(seconds=chunk_start),
                end=timedelta(seconds=chunk_end),
                content=chunk
            )
            subtitles.append(subtitle)

    return srt.compose(subtitles)


appold = FastAPI(debug=False)  # Vypnout debug pro produkci

appold.mount('/static', StaticFiles(directory='static'), name='static')
template = Jinja2Templates(directory='templates')

# Přednačtení nejpoužívanějšího modelu při startu
@appold.on_event("startup")
async def startup_event():
    # Přednahrajeme model "turbo" při startu
    get_model("turbo")
    logger.info("Aplikace připravena")


@appold.get('/', response_class=HTMLResponse)
def index(request: Request):
    return template.TemplateResponse('index.html', {
        "request": request, 
        "text": None,
        "gpu_available": torch.cuda.is_available(),
        "gpu_name": torch.cuda.get_device_name(0) if torch.cuda.is_available() else None
    })


@appold.post('/download/')
async def download_subtitle(
        request: Request,
        file: bytes = File(),
        model_type: str = Form("turbo"),  # Změna na turbo jako výchozí
        timestamps: Optional[str] = Form("True"),  # Změna na True jako výchozí
        filename: str = Form("subtitles"),
        file_type: str = Form("srt"),
        max_characters: int = Form(DEFAULT_MAX_CHARACTERS),
        translate_to: str = Form('english'),  # Změna na angličtinu jako výchozí
):
    temp_audio_file = 'temp_audio.mp3'
    
    try:
        # Uložení dočasného souboru
        with open(temp_audio_file, 'wb') as f:
            f.write(file)
        
        # Získání modelu z cache
        model = get_model(model_type)
        
        # GPU optimalizované nastavení pro transcribe
        transcribe_options = {
            "language": None,  # Automatická detekce jazyka
            "beam_size": 5,
            "best_of": 5,
            "temperature": 0,
            "compression_ratio_threshold": 2.4,
            "no_speech_threshold": 0.6,
            "condition_on_previous_text": True,
            "fp16": torch.cuda.is_available(),  # Float16 pouze s GPU
            "vad_filter": True,  # Voice Activity Detection pro rychlejší zpracování
            "vad_parameters": {
                "threshold": 0.5,
                "min_speech_duration_ms": 250,
                "max_speech_duration_s": float('inf'),
                "min_silence_duration_ms": 2000,
                "window_size_samples": 1024,
                "speech_pad_ms": 400
            }
        }
        
        # Transkripce s optimalizací
        logger.info(f"Začínám transkripci s modelem {model_type} na {device}")
        result = model.transcribe(temp_audio_file, **transcribe_options)
        logger.info("Transkripce dokončena")

        # Generování titulků
        subtitle_file = f"{filename}.{file_type}"
        
        with open(subtitle_file, "w", encoding='utf-8') as f:
            if timestamps == "True":
                if file_type == "srt":
                    f.write(make_srt_subtitles(result.segments, translate_to, max_characters))
                else:  # vtt
                    # Pro VTT s překladem
                    translated_segments = []
                    for seg in result.segments:
                        seg_copy = type(seg)()
                        for key, value in seg.__dict__.items():
                            setattr(seg_copy, key, value)
                        seg_copy.text = translate_text(seg.text.strip(), translate_to)
                        translated_segments.append(seg_copy)
                    
                    # Vytvoření nového result objektu s přeloženými segmenty
                    result.segments = translated_segments
                    f.write(result.to_vtt())
            else:
                translated_text = translate_text(result.text, translate_to)
                f.write(translated_text)

        # Odeslání souboru
        media_type = "application/octet-stream"
        response = StreamingResponse(
            open(subtitle_file, 'rb'),
            media_type=media_type,
            headers={'Content-Disposition': f'attachment;filename={subtitle_file}'}
        )
        
        return response
        
    except Exception as e:
        logger.error(f"Chyba při zpracování: {e}")
        raise
    finally:
        # Vyčištění dočasných souborů
        for temp_file in [temp_audio_file, subtitle_file]:
            if os.path.exists(temp_file):
                try:
                    os.remove(temp_file)
                except:
                    pass
        
        # Vyčištění GPU paměti
        if torch.cuda.is_available():
            torch.cuda.empty_cache()