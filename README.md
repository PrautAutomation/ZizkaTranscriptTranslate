## Webová stránka, která převádí řeč na text pomocí modelu Whisper ([Oficiální repozitář](https://github.com/openai/whisper))

## Hostování webových stránek na localhostu:

1. Naklonujte repozitář - `git clone https://github.com/PrautAutomation/ZizkaTranscriptTranslate.git`
2. Přejděte do adresáře repozitáře - `cd ZizkaTranscriptTranslate`
3. Vytvořte virtuální prostředí - `python3 -m venv venv`
4. Aktivujte prostředí - `source venv/bin/activate`/`. venv/bin/activate`
5. Požadavky na instalaci - `pip install -r requirements.txt`
6. Přejděte do adresáře src - `cd src`
7. Spusťte soubor `run.py` - `python3 run.py`
8. Přejděte do prohlížeče a zadejte `http://127.0.0.1:18666/`, pokud se prohlížeč neotevře

## Spuštění webu na localhostu s Dockerem
### Poprvé
1. Nainstalujte [Docker](https://docs.docker.com/engine/install/)
2. Naklonujte repozitář - `git clone https://github.com/PrautAutomation/ZizkaTranscriptTranslate.git`
3. Přejděte do adresáře repozitáře - `cd ZizkaTranscriptTranslate`
4. Vytvořte obraz Dockeru - `docker build -t appold .`
5. Spusťte kontejner Dockeru - `docker run --name app_container -p 18666:18666 appold`
6. Přejděte do prohlížeče a zadejte `http://127.0.0.1:18666/`

### Příště

1. Spusťte kontejner Docker - `docker start app_container`
2. Přejděte do prohlížeče a zadejte `http://127.0.0.1:18666/`
