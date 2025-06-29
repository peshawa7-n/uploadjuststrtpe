import os
import requests
from dotenv import load_dotenv
from pytube import YouTube

# Load StreamTape API credentials from .env
load_dotenv()
API_LOGIN = os.getenv("STREAMTAPE_API_USERNAME")
API_KEY = os.getenv("STREAMTAPE_API_KEY")


def download_youtube_video(yt_url, output_folder="downloads"):
    yt = YouTube(yt_url)
    video_stream = yt.streams.get_highest_resolution()
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    print(f"Downloading YouTube video: {yt.title}")
    file_path = video_stream.download(output_path=output_folder)
    print(f"✅ Download complete: {file_path}")
    return file_path


def get_upload_url():
    url = "https://api.streamtape.com/file/ul?login=79e10358ea0fdad85e40&key=QKkev1xQwmF0ZoQ"
    response = requests.get(url)
    data = response.json()
    if data['status'] == 200:
        return data['result']['url']
    else:
        raise Exception("Failed to get upload URL: " + str(data))


def upload_video(file_path):
    print(f"Uploading to StreamTape: {file_path}")
    upload_url = get_upload_url()
    with open(file_path, 'rb') as f:
        files = {'file1': (os.path.basename(file_path), f)}
        response = requests.post(upload_url, files=files)
        result = response.json()
        if result["status"] == 200:
            print("✅ Upload Success!")
            print("🎥 Video URL:", result["result"]["url"])
        else:
            print("❌ Upload Failed:", result)


if __name__ == "__main__":
    yt_url = "https://youtu.be/1Vk5MhPmnGE?si=FXTRPc78U85K8PBM".strip()
    try:
        video_path = download_youtube_video(yt_url)
        upload_video(video_path)
    except Exception as e:
        print(f"❌ Error: {e}")
