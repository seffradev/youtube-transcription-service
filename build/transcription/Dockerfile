FROM python:3.11-bookworm
WORKDIR /app
COPY ../../requirements.txt ./
RUN apt update && apt upgrade -y && apt install ffmpeg -y
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --upgrade yt-dlp
COPY ./cmd/transcription/ .
CMD [ "python", "./main.py" ]
