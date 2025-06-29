import os
import requests
from dotenv import load_dotenv
from pytube import YouTube

# Load MixDrop API credentials from .env
load_dotenv()
API_KEY = os.getenv("MIXDROP_API_KEY")  # MixDrop API key (use cookies if needed)


def download_youtube_video(yt_url, output_folder="downloads"):
    yt = YouTube(yt_url)
    video_stream = yt.streams.get_highest_resolution()
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    print(f"Downloading YouTube video: {yt.title}")
    file_path = video_stream.download(output_path=output_folder)
    print(f"✅ Download complete: {file_path}")
    return file_path


def upload_to_mixdrop(file_path):
    print(f"Uploading to MixDrop: {file_path}")
    upload_url = "https://api.mixdrop.co/upload"

    # You may need to pass your session or token via cookies or headers depending on MixDrop auth
    files = {"file": open(file_path, "rb")}
    data = {"api_key": API_KEY}  # if MixDrop supports this field, or handle session otherwise

    response = requests.post(upload_url, files=files, data=data)
    print("Status Code:", response.status_code)
    print("Response:", response.text)

    try:
        result = response.json()
        if result.get("status") == 200:
            print("✅ Upload Success!")
            print("🎥 Video URL:", result.get("result", {}).get("url"))
        else:
            print("❌ Upload failed:", result)
    except Exception as e:
        print("❌ Error parsing response:", e)


if __name__ == "__main__":
    yt_url = input("🔗 Enter YouTube video URL: ").strip()
    try:
        video_path = download_youtube_video(yt_url)
        upload_to_mixdrop(video_path)
    except Exception as e:
        print(f"❌ Error: {e}")
