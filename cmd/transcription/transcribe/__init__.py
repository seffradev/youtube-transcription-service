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
        info = ydl.extract_info(urls[0], download=False)

        if not info:
            raise ValueError("Failed to extract video info")

        id = info["id"]
        title = info["title"]
        filename = f"{title} [{id}].{codec}"
        error_code = ydl.download(urls)

    return filename

def remove_video(filename):
    subprocess.run(["rm", filename])

def transcribe(filename, language=None):
    model = whisper.load_model("medium")
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
