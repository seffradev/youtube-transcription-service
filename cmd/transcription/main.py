import subprocess
import sys
import yt_dlp
import whisper


def download_video(urls):
    if len(urls) > 1:
        print("Too many URLs. Can only handle one at a time")
        sys.exit(1)
    filename = ""
    codec = "mp3"
    ydl_opts = {
        "format": "m4a/bestaudio/best",
        "postprocessors": [{  # Extract audio using ffmpeg
            "key": "FFmpegExtractAudio",
            "preferredcodec": codec,
        }],
        "quiet": True,
        "external_downloader_args": ["-loglevel", "panic"],
        "noprogress": True,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        error_code = ydl.download(urls)
        info = ydl.extract_info(urls[0], download=False)
        id = info["id"]
        title = info["title"]
        filename = f"{title} [{id}].{codec}"
    return filename

def transcribe(filename, language=None):
    model = whisper.load_model("small")
    result = model.transcribe(filename)
    return result["text"]

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"usage: {sys.argv[0]} <url>")
        sys.exit(1)
    filename = download_video([sys.argv[1]])

    transcription = transcribe(filename)

    subprocess.run(["rm", filename])

    print(transcription)