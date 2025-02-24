import yt_dlp
import os
import pyfiglet
from colorama import Fore, Style

def print_banner():
    banner = pyfiglet.figlet_format("Video Rider", font="slant")  
    print(Fore.YELLOW + Style.BRIGHT + banner + Style.RESET_ALL)

print_banner()

def get_video_info(url):
    """ Retrieve video information and available formats """
    ydl_opts = {'quiet': True}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
    return info

def list_formats(info):
    """ Display available video qualities """
    formats = info.get('formats', [])
    available_formats = []
    print("\nAvailable formats:")
    for fmt in formats:
        if fmt.get('filesize'):
            size_mb = fmt['filesize'] / (1024 * 1024)  # Convert to MB
            available_formats.append((fmt['format_id'], fmt['format_note'], size_mb))
            print(f"{fmt['format_id']} - {fmt['format_note']} - {size_mb:.2f}MB")
    return available_formats

def download_video(url, format_id, is_audio):
    """ Download video or audio based on user selection """
    options = {
        'format': format_id, 
        'outtmpl': 'downloads/%(title)s.%(ext)s', 
    }
    
    if is_audio:
        options['format'] = 'bestaudio'
        options['postprocessors'] = [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }]

    with yt_dlp.YoutubeDL(options) as ydl:
        ydl.download([url])

if __name__ == "__main__":
    url = input("Enter video URL: ")
    info = get_video_info(url)

    choice = input("Do you want to download video or audio only? (video/audio): ").strip().lower()
    is_audio = choice == 'audio'

    if is_audio:
        format_id = 'bestaudio'
        size_mb = info['formats'][-1]['filesize'] / (1024 * 1024)  # Best audio quality
        print(f"\n📂 Estimated file size: {size_mb:.2f}MB")
    else:
        available_formats = list_formats(info)
        format_id = input("\nChoose the format ID you want to download: ").strip()
        size_mb = next((size for fid, _, size in available_formats if fid == format_id), None)
        if size_mb is None:
            print("❌ Invalid format selection!")
            exit()

    confirm = input(f"\n🔹 The file size will be approximately {size_mb:.2f}MB. Proceed? (y/n): ").strip().lower()
    if confirm == 'y':
        print("\n⏳ Downloading...")
        download_video(url, format_id, is_audio)
        print("\n✅ Download completed!")
    else:
        print("\n❌ Download canceled.")
      
