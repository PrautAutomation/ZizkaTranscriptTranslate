from pathlib import Path
from time import sleep
import uvicorn
import webbrowser
import torch
import logging
from multiprocessing import Process

# Nastavení loggingu
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def check_gpu():
    """Kontrola dostupnosti GPU"""
    if torch.cuda.is_available():
        logger.info(f"GPU detekována: {torch.cuda.get_device_name(0)}")
        logger.info(f"CUDA verze: {torch.version.cuda}")
        logger.info(f"Počet GPU: {torch.cuda.device_count()}")
        return True
    else:
        logger.warning("GPU není dostupná, aplikace poběží na CPU (pomalejší)")
        return False

def open_browser():
    sleep(3)  # Počkat na start serveru
    webbrowser.open('http://localhost:18666')

def run_localhost():
    uvicorn.run(
        'main:appold',
        host='0.0.0.0',
        port=18666,
        workers=1,  # Pouze 1 worker pro GPU
        log_level='info'
    )

if __name__ == '__main__':
    # Kontrola GPU při startu
    gpu_available = check_gpu()
    
    # Vytvoření potřebných složek
    Path("../data").mkdir(parents=True, exist_ok=True)
    Path("models").mkdir(parents=True, exist_ok=True)
    
    # Spuštění procesů
    open_browser_proc = Process(target=open_browser)
    run_localhost_proc = Process(target=run_localhost)
    
    run_localhost_proc.start()
    open_browser_proc.start()
    
    # Čekání na dokončení
    run_localhost_proc.join()