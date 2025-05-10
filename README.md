## Webová stránka, která převádí řeč na text pomocí modelu Whisper ([Oficiální repozitář](https://github.com/openai/whisper))

## Hostování webových stránek na localhostu:

1. Naklonujte repozitář - `git clone git@github.com:Kabanosk/whisper-website.git`
2. Přejděte do adresáře repozitáře - `cd whisper-website`
3. Vytvořte virtuální prostředí - `python3 -m venv venv`
4. Aktivujte prostředí - `source venv/bin/activate`/`. venv/bin/activate`
5. Požadavky na instalaci - `pip install -r requirements.txt`
6. Přejděte do adresáře src - `cd src`
7. Spusťte soubor `run.py` - `python3 run.py`
8. Přejděte do prohlížeče a zadejte `http://127.0.0.1:8000/`, pokud se prohlížeč neotevře

## Spuštění webu na localhostu s Dockerem
### Poprvé
1. Nainstalujte [Docker](https://docs.docker.com/engine/install/)
2. Naklonujte repozitář - `git clone git@github.com:Kabanosk/whisper-website.git`
3. Přejděte do adresáře repozitáře - `cd whisper-website`
4. Vytvořte obraz Dockeru - `docker build -t app .`
5. Spusťte kontejner Dockeru - `docker run --name app_container -p 80:80 app`
6. Přejděte do prohlížeče a zadejte `http://127.0.0.1:80/`

### Příště

1. Spusťte kontejner Docker - `docker start app_container`
2. Přejděte do prohlížeče a zadejte `http://127.0.0.1:80/`
