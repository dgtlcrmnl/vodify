import os
import sys
import subprocess
import shutil
from pathlib import Path

def install_streamlink():
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "streamlink"], check=True)
    except subprocess.CalledProcessError:
        print("Failed to install Streamlink. Please install it manually with:")
        print("pip install streamlink")
        sys.exit(1)

def find_streamlink():
    streamlink_path = shutil.which("streamlink")
    if streamlink_path:
        return streamlink_path
    try:
        username = os.getlogin()
        python_version = f"Python{sys.version_info.major}{sys.version_info.minor}"
        default_path = Path(f"C:/Users/{username}/AppData/Roaming/{python_version}/Scripts/streamlink.exe")
        if default_path.exists():
            return str(default_path)
    except Exception:
        pass
    return None

def download_twitch_vod():
    install_streamlink()
    streamlink_path = find_streamlink() or "streamlink"
    
    vod_url = input("Enter the Twitch VOD URL: ")
    quality = input("Enter desired quality (e.g., best, 720p, 480p): ")
    output_filename = input("Enter the output file name: ")
    
    if not output_filename.endswith(".mp4"):
        output_filename += ".mp4"

    command = [
        streamlink_path,
        vod_url, quality,
        "--hls-live-restart",
        "--retry-streams", "5",
        "-o", output_filename
    ]
    
    try:
        subprocess.run(command, check=True)
        print(f"Download complete: {output_filename}")
    except Exception as e:
        print(f"Error: {str(e)}")
        print("Make sure the URL is correct and the VOD is available.")

if __name__ == "__main__":
    download_twitch_vod()