import subprocess
import sys
import whisper
import yt_dlp

def download_video(urls) -> str:
    if len(urls) > 1:
        raise ValueError("Too many URLs, only one is allowed")

    filename = ""
    codec = "mp3"
    ydl_opts = {
        "format": f"{codec}/bestaudio/best",
        "postprocessors": [{  # Extract audio using ffmpeg
            "key": "FFmpegExtractAudio",
            "preferredcodec": codec,
        }],
        "quiet": True,
        "external_downloader_args": ["-loglevel", "panic"],
        "noprogress": False,
        "outtmpl": "%(id)s.%(ext)s",
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        error_code = ydl.download(urls)
        info = ydl.extract_info(urls[0], download=False)

        if not info:
            raise ValueError("Failed to extract video info")

        id = info["id"]
        filename = f"{id}.{codec}"

    return filename

def remove_video(filename):
    subprocess.run(["rm", filename])

def transcribe(filename, language=None):
    model = whisper.load_model("small")
    result = model.transcribe(filename)
    return result["text"]

# This is a test function to check if the transcribe function
# works. It is not part of the main program. It is executed like
# a POSIX-compliant script, i.e. `python3 __init__.py <url>`
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"usage: {sys.argv[0]} <url>")
        sys.exit(1)

    filename = download_video([sys.argv[1]])
    transcription = transcribe(filename)
    remove_video(filename)
    print(transcription)
