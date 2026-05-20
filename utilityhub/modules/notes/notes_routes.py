from flask import render_template, Flask, send_from_directory, Blueprint, redirect, request

from modules.notes.notes_service import NotesService
#defining the blue print
notes_bp = Blueprint('notes', __name__)


notes_service = NotesService()

@notes_bp.route("/Notes",  methods=["GET","POST"])
def Notes():
    keyword = request.form.get("q")
    tag = request.args.get("tag")
    
    # load notes:
    if keyword:
        notes = notes_service.search_notes(keyword)
    elif tag:
        notes = notes_service.search_by_tag(tag)
    else:
        notes = notes_service.list_notes()


    notes['Created_At'] = notes["Created_At"].dt.date
    notes = notes.reset_index().to_dict("records") # orient="records" -> list of dicts
    # reset index because to_dict delete the index 

    #color:
    tag_colors = {
        "General": "#6f42c1",   # purple
        "Work": "#0d6efd",      # blue
        "Dev": "#198754",       # green
        "Reading": "#0dcaf0",   # cyan
        "Personal": "#d63384",  # pink
    }
    snippets = []
    colors = []
    for note in notes:
        note["Content"] = str(note["Content"]) if str(note["Content"]) != "nan" else ""

        snippet = note["Content"] if len(note["Content"]) < 60 else note["Content"][:60] + "..."
        snippets.append(snippet)

        # get colors
        color = tag_colors.get(note["Tag"], "info")
        colors.append(color)



    # i want to iterate over both list simulaneously -> ZIP
    data = zip(notes,snippets, colors)



    return render_template("notes.html", current_page="Notes", data=data, notes_count= len(notes), keyword=keyword, tag=tag)


@notes_bp.route("/Notes/new", methods=["GET","POST"])
def new():
    if request.method == "POST":
        return redirect('/Notes')


    return render_template("note_form.html", current_page="Notes", data=None)


@notes_bp.route("/Notes/create", methods=["POST", "GET"])
def createNote():
    if request.method == "GET":
        return redirect('/Notes')


    title = request.form.get("title")
    Tag = request.form.get("Tag")
    content = request.form.get("content")

    if content == "":
        return redirect("/Notes")

    if title == "":
        title="Untitled Note"


    
    notes_service.save_note(title, content, Tag ) 

    return redirect("/Notes")



@notes_bp.route("/Notes/modify/<id>", methods=["POST", "GET"])
def modify(id):
    if request.method == "GET":
        return redirect('/Notes')

    id = int(id)
    note = notes_service.get_note_by_id(id)
    note["Id"] = id

    return render_template("note_form.html", current_page="Notes", data=note)



@notes_bp.route("/Notes/delete/<id>", methods=["POST", "GET"])
def delete(id):
    if request.method == "GET":
        return redirect('/Notes')

    id = int(id)
    notes_service.delete_note(id)
    return redirect("/Notes")


@notes_bp.route("/Notes/update/<id>", methods=["POST", "GET"])
def update(id):
    if request.method == "GET":
        return redirect('/Notes')


    title = request.form.get("title")
    Tag = request.form.get("Tag")
    content = request.form.get("content")

    if content == "":
        return redirect("/Notes")

    if title == "":
        title="Untitled Note"

    notes_service.save_note(title, content, Tag, int(id))

    return redirect("/Notes")