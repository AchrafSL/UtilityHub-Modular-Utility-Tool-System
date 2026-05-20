from flask import render_template, Flask, send_from_directory, Blueprint, request, Response, redirect

from modules.downloader.downloader_service import MediaDownloaderService

import threading
import json
import time
import os


#defining the blue print
downloader_bp = Blueprint('downloader', __name__)

downloader_service = MediaDownloaderService()

download_queue = []
download_progress = {}
nbr_of_downloads = 0
is_currently_downloading = False # mutex 
current_worker_id  = None


@downloader_bp.route("/Downloader")
def Downloader():
    return render_template("downloader.html", current_page="Downloader")


@downloader_bp.route("/Downloader/fetchFormats", methods=["POST","GET"])
def fetchFormats():
    if request.method == "POST":

        fetchError = "Fetch Failed! Check your URL and try again."
        url = request.form.get("link")

        try:
            info = downloader_service.get_media_info(url)
            print(info['metadata']['title'])
        except Exception as e:
            return render_template("downloader.html", fetchError=fetchError, current_page="Downloader")

        if info is None:
            return render_template("downloader.html", fetchError=fetchError, current_page="Downloader")


        return render_template("downloader.html", current_page="Downloader", metadata=info['metadata'], formats=info['formats'], url=url)
    
    else:
        return redirect('/Downloader')



@downloader_bp.route("/downloadProcess", methods=["POST","GET"])
def downloadProcess():
    if request.method == "POST":
        global nbr_of_downloads
        nbr_of_downloads += 1
        idI = nbr_of_downloads

        url = request.form.get("url")
        format_id = request.form.get("format_id")
        is_audio = request.form.get("is_Audio")
        
        info = {
            "id": idI,
            "url":url,
            "format_id":format_id,
            "is_Audio":(is_audio == "True")
        }
        global download_queue
        download_queue.append(info)
        
        # process the download (wait or start download)
        process_queue()

        # Return the rendered HTML row as a string
        return render_template("queue_row.html", id=idI, url=url)

    else:
        return redirect('/Downloader')




def process_queue():
    # check if downloading, no one waiting -> stop
    global is_currently_downloading

    if is_currently_downloading or not download_queue:
        return 

    # else start downloading first one in Queue (FIFO):
    is_currently_downloading = True  # to stop other workers 
    info = download_queue.pop(0)

    global current_worker_id # when there is an assignment always use the global 

    current_worker_id = info['id'] # save current worker to kill if op cancelled


    # start downloading:
    threading.Thread(target=start_download, args=[info['url'], info['format_id'],progress_hook , info['is_Audio']]).start()


def start_download(url, format, hook, is_audio):
    global is_currently_downloading
    global current_worker_id
    
    status, outfileName = downloader_service.download_media(url, format, hook, is_audio)
    
    if status == "SUCCESS":
        filename = os.path.basename(outfileName)
        download_progress[current_worker_id] = f"Done!|{filename}"

    else:
        download_progress[current_worker_id] = "Error!"


    # when download finish
    is_currently_downloading = False
    
    # check next:
    process_queue()



def progress_hook(data):
    if data.get('status') == 'downloading':
        global current_worker_id
        downloaded = data.get('downloaded_bytes', 0)
        total = data.get('total_bytes') or data.get('total_bytes_estimate', 0)
        speed = data.get('speed', 0)
        estimated_time = data.get('eta', 0)

        percent = ( downloaded / total * 100) if total > 0 else 0
        speed_mb = speed / (1024 * 1024) if speed else 0
        total_mib = total / (1024 * 1024)

        progress_str = f"{percent:.1f}% of {total_mib:.2f}MiB at {speed_mb:.2f}MiB/s ETA {estimated_time}s"
        download_progress[current_worker_id] = progress_str




@downloader_bp.route("/Downloader/progress")
def progress():
    
    def generator():
        """
        Unlike return (which sends data and kills the function), yield sends
            data but pauses the function right where it is.
        """
    
        while True:
            # send progress for every 0.5s
            time.sleep(0.5)
            # json.dumps (convert dict to json)
            yield f"data:{json.dumps(download_progress)}\n\n"


    """
    The Iterator: Flask's Response object takes that generator and acts as the Iterator.
     It basically says: "I will keep calling next() on this generator as long as the 
     HTTP connection is open. Every time I call it, the generator wakes up, runs until the
      next yield, and then goes back to sleep."
    """
    return Response(generator(), mimetype='text/event-stream')



@downloader_bp.route("/Downloader/get_file/<path:filename>")
def get_file(filename):
    # This sends the file from output folder to the browser
    directory = downloader_service.output_path
    return send_from_directory(directory, filename, as_attachment=True)

























"""
Technical Overview: Server-Sent Events (SSE)
Server-Sent Events (SSE) is a standardized web technology, part of the HTML5 specification
, designed to enable unidirectional, real-time data streaming from a server 
to a client over a persistent HTTP connection. It allows a server to push updates
to a web page automatically, eliminating the need for inefficient client-side polling.



1. Fundamental Mechanism
Unlike traditional HTTP requests, which follow a request-response cycle and close 
the connection immediately after completion, SSE maintains an open, persistent connection.
The client initiates the connection using the EventSource API. The server responds with
a specialized MIME type (text/event-stream) and keeps the connection active to transmit
a sequence of data fragments.



2. Protocol and Data Framing
SSE operates over standard HTTP/HTTPS and adheres to a strict message framing protocol:

MIME Type: The response header must specify Content-Type: text/event-stream.

Message Format: Each event is transmitted as a plain-text block starting with the data:  
prefix, followed by the message payload, and terminated by
two consecutive newline characters (\n\n).

Event Types: Optionally, servers can include an event:  field to categorize messages, 
which the client can then filter using specific listeners.



3. resume:
SSE keeps a persistent HTTP connection open so the server can push data to the client 
in real-time without polling. The client connects once via the EventSource API, and the server
 streams plain-text events formatted as data: ...\n\n with Content-Type: text/event-stream.

Key advantages over alternatives: simpler than WebSockets (one-way only), auto-reconnects 
on drop, and works through firewalls since it uses standard HTTP ports.

In this app, it's used to stream download progress (percentage, speed, ETA) from the backend
 worker thread to the frontend UI in real-time.

"""