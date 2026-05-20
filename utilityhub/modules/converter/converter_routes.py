from flask import render_template, Flask, send_from_directory, Blueprint, request, send_file, redirect
import os
from modules.converter.converter_service import ConverterService
import time
import threading

converter_service = ConverterService()


#defining the blue print
converter_bp = Blueprint('converter', __name__)


@converter_bp.route("/Converter")
@converter_bp.route("/")
def Converter():
    return render_template("converter.html", current_page="Converter")

UPLOAD_FOLDER = r"C:\Users\achra\OneDrive\Desktop\UIT_master\Uit Master projects\python s1\UtilityHub – Application Modulaire d’Outils Utilitaires (Desktop + Web)\utilityhub\data\uploads"

@converter_bp.route("/ConvertUpload", methods = ["POST","GET"])
def ConvertUpload():
    if request.method == "POST":
        file = request.files["fileInp"]

        # save the file
        if file and file.filename != "":
            filepath = os.path.join(UPLOAD_FOLDER, file.filename)
            file.save(filepath)

            path = converter_service.output_path

            # load the page with the possible conversions
            return render_template("converter.html", current_page='Converter', formats=get_available_formats(file), filename=file.filename)

    else:
        return redirect('/Converter')


@converter_bp.route("/ConvertProcess", methods = ["POST","GET"])
def ConvertProcess():
    if request.method == "POST":
        file_name = request.form.get("filename")

        ext = os.path.splitext(file_name)[1].lower()
        file_path = os.path.join(UPLOAD_FOLDER, file_name)

        selected_format = request.form.get("format")
        print(selected_format)
        try:
            ret = None
            match selected_format:
                case "PDF": 
                    if ext == ".md":
                        ret = converter_service.convert_md_to_pdf(file_path)
                    elif ext == ".txt":
                        ret = converter_service.convert_txt_to_pdf(file_path)
                case "MP3": ret = converter_service.convert_mp4_to_mp3(file_path)
                case "SVG": ret = converter_service.convert_to_svg(file_path)
                case "JPG": ret = converter_service.convert_to_jpg(file_path)
                case "PNG": ret = converter_service.convert_to_png(file_path)
                case _: print("ext not supported")
        except Exception as e :
            import traceback

            print("convertion error")
            print(f"Variables: filename='{file_name}', format='{selected_format}', path='{file_path}'")
            traceback.print_exc()

            return render_template("converter.html", current_page="Converter", error="Conversion failed or format not supported!")

        if ret and ret != -1:
            threading.Thread(target=delete_file_later, args=[file_path]).start()

            return send_file(ret, as_attachment=True)
        else:
            print("ret error")
            return render_template("converter.html", current_page="Converter", error="Conversion failed or format not supported!")

    else:
        return redirect('/Converter')







def get_available_formats(file):
    ext = os.path.splitext(file.filename)[1].lower()


    formats_map = {
        '.md': ['PDF'],
        '.mp4': ["MP3"],
        ".png": ["JPG", "SVG"],  
        ".jpg": ["PNG", "SVG"],  
        ".jpeg": ["PNG", "SVG"], 
        ".webp": ["JPG", "PNG", "SVG"], 
        ".bmp": ["JPG", "PNG"],  
        ".tiff": ["JPG"]      
    }

    return formats_map.get(ext, [])



   

def delete_file_later(file, delay=60):
    time.sleep(delay)
    
    try:
        if os.path.exists(file):
            os.remove(file)
            print(f"DELETING SUCCESS {file}")
    except Exception as e:
        print(f"Could not delete {file}: {e}")
