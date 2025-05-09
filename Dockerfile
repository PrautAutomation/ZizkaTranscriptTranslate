FROM python:3.9
WORKDIR /appold

RUN apt-get -y update
RUN apt-get -y upgrade
RUN apt-get install -y ffmpeg

COPY requirements.txt /appold

RUN pip install uv
RUN uv pip install --system -r requirements.txt

COPY src/ /appold

CMD ["uvicorn", "main:appold", "--host", "0.0.0.0", "--port", "18666"]
