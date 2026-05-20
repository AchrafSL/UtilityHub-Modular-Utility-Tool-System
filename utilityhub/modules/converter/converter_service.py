from PIL import Image
import vtracer
from markdown import markdown
from xhtml2pdf import pisa
from core.history_manager import HistoryManager
from core.settings_manager import SettingsManager
import os
import subprocess

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



class ConverterService:

    def __init__(self):
        self.settingsManager = SettingsManager()
        self.historyManager = HistoryManager("converter")

        self.output_path = ""


    def _refresh_settings(self):
        self.output_path = self.settingsManager.get_setting("output_paths", "converter")



    @refresh_settings
    def convert_md_to_pdf(self, input_file_path):
        # Check input_file_path extensions
        if not input_file_path.lower().endswith('.md'):
            return -1


        # Read the MD:
        with open(input_file_path, "r", encoding="utf-8") as f:
            md_text = f.read()

        # md to html
        html_content = markdown(md_text, extensions = ['fenced_code'])
        
        # reminder: <pre>: Display this text exactly as written.
        styled_html = f"""
        <html>
        <head>
            <style>
                body {{ font-family: Helvetica, Arial, sans-serif; font-size: 11pt; line-height: 1.5; color: #333; }}
                h1, h2, h3 {{ color: #1f4068; border-bottom: 1px solid #1f4068; padding-bottom: 5px; }}
                pre {{ background-color: #f4f4f4; padding: 10px; border-radius: 5px;white-space: pre-wrap; word-wrap: break-word; }}
                code {{ font-family: Courier, monospace; color: #1f4068; background-color: #f7f7f7; padding: 2px 4px; border-radius: 3px; }}
            </style>
        </head>
        <body>
            {html_content}
        </body>
        </html>
        """

        output_file_name = os.path.basename(input_file_path).rsplit('.', 1)[0] + ".pdf"
        output_file = os.path.join(self.output_path, output_file_name)

        # convert html to pdf
        with open(output_file, "wb") as file_out:
            pisa.CreatePDF(styled_html, dest=file_out)

        print("Markdown conversion complete!")

        # Save history:
        self.historyManager.add_record(input_file_path, output_file)
        return output_file


    @refresh_settings
    def convert_txt_to_pdf(self, input_file_path):
        if not input_file_path.lower().endswith('.txt'):
            return -1

        with open(input_file_path, "r", encoding="utf-8") as f:
            text_content = f.read()

        # Wrap in pre-tag for plain text preservation
        html_content = f"""
        <html>
            <body>
                <pre style='white-space: pre-wrap; font-family: Helvetica; font-size: 11pt;'>
                {text_content}
                </pre>
            </body>
        </html>
        """

        output_file_name = os.path.basename(input_file_path).rsplit('.', 1)[0] + ".pdf"
        output_file = os.path.join(self.output_path, output_file_name)

        with open(output_file, "wb") as file_out:
            pisa.CreatePDF(html_content, dest=file_out)

        print("Text conversion complete! ")

        # save history:
        self.historyManager.add_record(input_file_path, output_file)
        return output_file



    
    @refresh_settings
    def convert_to_jpg(self, input_file_path):
        # Check input_file_path extensions
        valid_ext = (".png", ".webp", ".bmp", ".tiff")
        if not input_file_path.lower().endswith(valid_ext):
            return -1


        output_file_name = os.path.basename(input_file_path).rsplit('.', 1)[0] + ".jpg"
        output_file = os.path.join(self.output_path, output_file_name)

        with Image.open(input_file_path) as img:
            # Convert RGBA (transparency) to RGB (flat color)

            if img.mode in ("RGBA", "P"):
                img = img.convert("RGB")
            img.save(output_file, "JPEG", quality=95)  # .rsplit(separator, maxsplit)

        
        print("jpg conversion complete! ")

        # Save history:
        self.historyManager.add_record(input_file_path, output_file)

        return output_file



    @refresh_settings
    def convert_to_png(self, input_file_path):
        # Check extensions:
        valid_ext = (".jpg", ".jpeg", ".webp", ".bmp")
        if not input_file_path.lower().endswith(valid_ext):
            return -1

        output_file_name = os.path.basename(input_file_path).rsplit('.', 1)[0] + ".png"
        output_file = os.path.join(self.output_path, output_file_name)
    
        with Image.open(input_file_path) as img:
            img.save(output_file, "PNG")

        print("png conversion complete! ")
        # Save history:
        self.historyManager.add_record(input_file_path, output_file)

        return output_file

    


    @refresh_settings
    def convert_to_svg(self, input_file_path):
        # Check extensions:
        valid_ext =(".jpg", ".jpeg", ".png", ".webp")
        if not input_file_path.lower().endswith(valid_ext):
            return -1

        output_file_name = os.path.basename(input_file_path).rsplit('.', 1)[0] + ".svg"
        output_file = os.path.join(self.output_path, output_file_name)

        try:
            # It converts pixels into mathematical SVG paths
            vtracer.convert_image_to_svg_py(
                input_file_path,   # Input Path
                output_file,       # Output Path
                "color",           # Colormode (color vs binary)
                "stacked",         # Hierarchical (stacked vs cutout)
                "spline",          # Mode (spline, polygon, none)
                4,                 # Filter Speckle
                6,                 # Color Precision
                60,                # Corner Threshold
                4,                 # Gradient Step
                2,                 # Path Precision
                10,                # Max Iterations
                45,                # Splice Threshold
                10                 # Segment Length
            )
        except Exception as e:
            print(f"vtracer exception {e}")

   
        
        print("svg conversion complete! ")

        # Save history:
        self.historyManager.add_record(input_file_path, output_file)

        return output_file


    
    @refresh_settings
    def convert_mp4_to_mp3(self, input_file_path):
        out_name = os.path.basename(input_file_path).rsplit('.', 1)[0] + ".mp3"
        out_path = os.path.join(self.output_path, out_name)

        # -i: Input, -q:a 0: Best quality, -map a: Audio only, -y: Overwrite existing
        cmd = [
            FFMPEG_PATH, 
            "-i", input_file_path, 
            "-q:a", "0", 
            "-map", "a", 
            out_path, 
            "-y" 
        ]
        try:

            # creationflags=0x08000000 to hide cmd window
            # check=True for non slient crashes
            subprocess.run(cmd, check=True, creationflags=0x08000000) 

            self.historyManager.add_record(input_file_path, out_path)

            print("MP3 Extraction Complete!")

            return out_path
        except Exception as e:
            print(f"FFmpeg Error: {e}")
            return -1
