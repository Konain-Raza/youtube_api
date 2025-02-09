from pytube import YouTube

def download_video(url, output_path="downloads/"):
    try:
        yt = YouTube(url)
        print(f"Downloading video: {yt.title}...")

        # Get the highest resolution stream
        video_stream = yt.streams.get_highest_resolution()
        video_stream.download(output_path)
        
        print("✅ Video downloaded successfully!")
    except Exception as e:
        print(f"❌ Error: {e}")

def download_audio(url, output_path="downloads/"):
    try:
        yt = YouTube(url)
        print(f"Downloading audio: {yt.title}...")

        # Get the audio stream
        audio_stream = yt.streams.filter(only_audio=True).first()
        audio_stream.download(output_path)

        print("✅ Audio downloaded successfully!")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    video_url = input("Enter YouTube URL: ")

    choice = input("Do you want to download (1) Video or (2) Audio? Enter 1 or 2: ")

    if choice == "1":
        download_video(video_url)
    elif choice == "2":
        download_audio(video_url)
    else:
        print("❌ Invalid choice! Please enter 1 or 2.")
