from transcribe import download_video, transcribe, remove_video

def main():
    url = input("Enter the URL of the video: ")
    filename = download_video([url])
    transcription = transcribe(filename)
    remove_video(filename)
    print(transcription)

if __name__ == "__main__":
    main()
