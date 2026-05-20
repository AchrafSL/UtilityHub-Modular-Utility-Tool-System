import yt_dlp 
from core.history_manager import HistoryManager 
from core.settings_manager import SettingsManager
import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
FFMPEG_PATH = os.path.join(BASE_DIR, "tools", "ffmpeg.exe")



def refresh_settings(func):
    def wrapper(self, *args, **kwargs):
        # "Before method"
        self._refresh_settings()
        result = func(self, *args, **kwargs)
        # "After method"
        return result
    return wrapper


class MediaDownloaderService:
    def __init__(self):
        self.settingsManager = SettingsManager()
        self.historyManager = HistoryManager("downloader")

        self.output_path = ""
        self.cookies_browser = "firefox" 


    def _refresh_settings(self):
        self.output_path = self.settingsManager.get_setting("output_paths", "downloader")
        try:
            self.cookies_browser = self.settingsManager.get_setting("preferences", "downloader_browser")
        except KeyError:
            self.cookies_browser = "firefox"
        



    @refresh_settings
    def get_media_info(self, url):
        try:
            ydl_opts = {
                "quiet":True, 
                'no_warnings': True,
                "noplaylist": True,    
                'restrictfilenames': True,
                'cookiesfrombrowser': (self.cookies_browser,),
                'verbose': True,
                'extract_flat': False,
                'nocheckcertificate': True,
            }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)  
                return {
                    "metadata": {
                        "title": info.get("title", "Unknown Title"),
                        "duration": info.get("duration", 0),
                        "thumbnail": info.get("thumbnail"),
                        "uploader": info.get("uploader","Unknown")
                    },
                    "formats": self.get_available_formats(info)
                }

        except:
            # Error: try again (maybe url not functionning)
            return None

    

    def get_available_formats(self, info):
        
        formats = []
        for format in info.get("formats",[]):

            vcodec = format.get("vcodec")
            acodec = format.get("acodec")

            is_audio = (vcodec == "none" or vcodec is None)


            # "vcodec" (video codec) or "acodec" (audio codec)
            if vcodec != "none" or acodec != "none":                
                formats.append({
                    "format_id": format.get("format_id"),
                    "ext": format.get("ext"),
                    "resolution": "Audio" if is_audio else (format.get("format_note") or format.get("resolution") or "Video")
                })

        return formats



    @refresh_settings
    def download_media(self, url, format_choice, progress_hook, is_audio=False):
        """
        In yt_dlp, a progress_hook is a function that gets called repeatedly
         while the download is running. It lets you track progress
          (percentage, speed, ETA, etc.) in real time.
        """
        output_filename = None 


        try:
            if is_audio:
                # Try specific choice, then any best audio
                final_format = f"{format_choice}/bestaudio/best"

            else:
                # try specific choice + best audio
                # try specific choice alone (combined or no audio)
                # try overall best video + best audio
                # try any 'best' format
                final_format = f"({format_choice}+bestaudio)/{format_choice}/bestvideo+bestaudio/best"



            ydl_opts = {
                'ffmpeg_location': FFMPEG_PATH,
                "format":final_format, # (format_id)
                "outtmpl": f"{self.output_path}/%(title)s-%(ext)s.%(ext)s",
                "progress_hooks": [progress_hook],
                "merge_output_format": "mp4", 
                """
                # tells yt-dlp:
                   If you have to stitch multiple files together (like HD video + audio),
                     please put the final result inside an mp4 container.
                """

                "noplaylist": True,    # Ensure it doesn't try to fetch a whole playlist
                'restrictfilenames': True,
                'cookiesfrombrowser': (self.cookies_browser,),
                'nocheckcertificate': True,
            }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])

                info = ydl.extract_info(url, download=False)

                output_filename = ydl.prepare_filename(info)

                # Save history:
                self.historyManager.add_record(url, output_filename )

                return "SUCCESS", output_filename


        except Exception as e:
            return "ERROR", output_filename # to delete the file
