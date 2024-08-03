import os
import logging
from yt_dlp import YoutubeDL


class Downloader:
    def __init__(self, download_dir="../data/downloads"):
        self.download_dir = download_dir
        self.YDL_OPTIONS = {
            'format': 'bestaudio/best',
            'outtmpl': os.path.join(self.download_dir, 'downloaded_audio.%(ext)s')
        }
        self.FFMPEG_OPTIONS = {
            'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
            'options': '-vn -nostdin'
        }

    def search_yt(self, item, extension='mp3', progress_callback=None):
        self.YDL_OPTIONS['outtmpl'] = os.path.join(self.download_dir, f'downloaded_audio.{extension}')
        
        def progress_hook(d):
            if progress_callback:
                progress_callback(d['status'], d.get('downloaded_bytes', 0), d.get('total_bytes', 0))
        
        self.YDL_OPTIONS['progress_hooks'] = [progress_hook]
        
        with YoutubeDL(self.YDL_OPTIONS) as ydl:
            try:
                info = ydl.extract_info(f"ytsearch:{item}", download=True)['entries'][0]
            except Exception as e:
                logging.error(f"Error occurred while extracting info from YouTube: {e}")
                return False
            
        audio_url = None
        for format in info['formats']:
            if format.get('acodec') and format['acodec'].lower() != 'none':
                audio_url = format['url']
                break
        
        if audio_url is None:
            logging.error("No audio format found for the given video")
            return False
        
        return {'source': audio_url, 'title': info['title']}
    
    def get_file(self, url, title, extension='mp3'):
        os.system(f"ffmpeg -i {url} -vn -ab 128k -ar 44100 -y {title}.{extension}")
        return f"{title}.{extension}"
