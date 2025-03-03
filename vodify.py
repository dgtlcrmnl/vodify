import os
import sys
import subprocess
import shutil
from pathlib import Path

VOD_DIR = "Downloaded VODs"
PROCESSED_SUFFIX = "_processed"

def setup_directories():
    Path(VOD_DIR).mkdir(parents=True, exist_ok=True)

def install_streamlink():
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "streamlink"], 
                        check=True,
                        stdout=subprocess.DEVNULL,
                        stderr=subprocess.DEVNULL)
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

def process_with_ffmpeg(input_path):
    try:
        path = Path(input_path)
        processed_path = path.parent / f"{path.stem}{PROCESSED_SUFFIX}{path.suffix}"

        ffmpeg_cmd = [
            "ffmpeg",
            "-y",
            "-i", str(input_path),
            "-c:v", "copy",
            "-c:a", "copy",
            str(processed_path)
        ]

        subprocess.run(ffmpeg_cmd, check=True, capture_output=True)
        print(f"Processed video saved to: {processed_path}")

        input_path.unlink()
        print(f"Original VOD deleted: {input_path}")

        return processed_path
    except subprocess.CalledProcessError as e:
        print(f"FFmpeg processing failed: {e.stderr.decode()}")
        return None

def download_twitch_vod():
    setup_directories()
    install_streamlink()
    streamlink_path = find_streamlink() or "streamlink"
    
    vod_url = input("Enter the Twitch VOD URL: ")
    quality = input("Enter desired quality (e.g., best, 720p, 480p): ")
    output_filename = input("Enter the output file name: ")
    
    if not output_filename.endswith(".mp4"):
        output_filename += ".mp4"
    
    output_path = Path(VOD_DIR) / output_filename

    command = [
        streamlink_path,
        vod_url, quality,
        "--hls-live-restart",
        "--retry-streams", "5",
        "-o", str(output_path)
    ]
    
    try:
        print("Starting download...")
        subprocess.run(command, check=True)
        print(f"Original VOD saved to: {output_path}")
        
        processed_path = process_with_ffmpeg(output_path)
        if processed_path:
            print(f"Processed VOD saved to: {processed_path}")
        else:
            print("Processing with FFmpeg failed.")
            
    except Exception as e:
        print(f"Error: {str(e)}")
        print("Possible issues:")
        print("- Invalid URL/VOD not available")
        print("- Network connectivity problems")
        print("- Disk space limitations")

if __name__ == "__main__":
    download_twitch_vod()
