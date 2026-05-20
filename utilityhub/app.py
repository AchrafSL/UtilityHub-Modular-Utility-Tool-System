from flask import render_template, Flask, send_from_directory, Blueprint, redirect

from modules.converter.converter_routes import converter_bp
from modules.downloader.downloader_routes import downloader_bp
from modules.notes.notes_routes import notes_bp
from modules.todo.todo_routes import todo_bp

from core.csv_manager import CsvManager
from core.history_manager import HistoryManager
import os
import pandas as pd

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
HISTORY_PATH = os.path.join(BASE_DIR, "data", "history.csv")

csv_manager = CsvManager(HISTORY_PATH)

template_folder="web/templates"
static_folder = "web/static"

# __name__ helps flask locate static and templates
# because __name__ if imported as module it prints the file name
# else if you run the file directly it prints __main__

app = Flask(__name__,template_folder=template_folder, static_folder=static_folder)


"""
Flask Blueprints are a way to organize your app into smaller,
 reusable modules instead of putting everything in one file.

Think of a blueprint like a mini Flask app inside your main app.
Each blueprint can have:
    its own routes
    templates
    static files
"""

# register the blueprints in app.py
app.register_blueprint(converter_bp)
app.register_blueprint(downloader_bp)
app.register_blueprint(notes_bp)
app.register_blueprint(todo_bp)

"""
concequences:
    @converter_bp.route() instead of @app.route
    and url_for('converter.Converter') instead of url_for('Converter')

"""


# history routes are in app.py







@app.route("/History", methods=["POST","GET"])
def History():
    history = csv_manager.load_csv()
    history['Request'] = history['Request'].apply(os.path.basename)
    history['Response'] = history['Response'].apply(os.path.basename)
    history["Date"] = pd.to_datetime(history["Date"]).dt.strftime("%Y-%m-%d %H:%M")
    history = history.sort_values(by="Date", ascending=False).to_dict("records")


    tool_colors = {
        "notes": ("#513b02", "#fcd53f"),       # Dark Gold bg, Yellow text
        "downloader": ("#471317", "#ff4d4d"),  # Dark Red bg, Bright Red text
        "converter": ("#08354c", "#4db8ff"),   # Dark Blue bg, Light Blue text
        "todo": ("#124021", "#42d667")         # Dark Green bg, Light Green text
    }

    colors = []
    for row in history:
        bg, text = tool_colors.get(row['Tool'], ("#2b2b2b", "#b0b0b0"))
        colors.append((bg, text))



    data = list(zip(history,colors))
    return render_template("history.html", current_page="History", data=data)





@app.route("/History/clear", methods=["POST"])
def clearHistory():
    history_manager_converter = HistoryManager("converter")
    history_manager_todo = HistoryManager("todo")
    history_manager_notes = HistoryManager("notes")
    history_manager_downloader = HistoryManager("downloader")

    history_manager_converter.clear_history()
    history_manager_todo.clear_history()
    history_manager_notes.clear_history()
    history_manager_downloader.clear_history()

    return redirect("/History")










# route that serves assets:
@app.route("/assets/<path:filename>") # path: is a converter so flask can still real after the slashes because normaly it stops as soon as seeing a forward / 
def serve_assets(filename):
    return send_from_directory('assets', filename)

if __name__ == '__main__':
    app.run(debug=True)