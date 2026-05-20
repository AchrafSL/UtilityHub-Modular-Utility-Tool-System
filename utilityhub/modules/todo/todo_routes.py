from flask import redirect
from flask import render_template, Flask, send_from_directory, Blueprint, request
from modules.todo.todo_service import TodoService



#defining the blue print
todo_bp = Blueprint('todo', __name__)

todo_service  = TodoService()

@todo_bp.route("/Todo", methods=["GET", "POST"])
def Todo():
    keyword = request.form.get("q")
    tag = request.args.get("tag")

    if keyword:
        tasks = todo_service.search_tasks(keyword)
    elif tag and tag != "All":
        tasks = todo_service.search_by_status(tag)
    else:
        tasks = todo_service.get_tasks()

    dataActive = tasks[ tasks['Status'].isin(['Pending', 'In-progress'])].reset_index().to_dict("records")
    dataDone = tasks[ tasks['Status'] == 'Done'].reset_index().to_dict("records")

    active_count = len(dataActive)
    done_count = len(dataDone)


    return render_template("todo.html", current_page="Todo", tag=tag, keyword=keyword, dataActive=dataActive, dataDone=dataDone, task_count=len(tasks),active_count=active_count, 
                       done_count=done_count)



@todo_bp.route("/Todo/new", methods=["GET", "POST"])
def newTask():
    if request.method == "GET":
        return redirect("/Todo")

    task_desc = request.form.get("task_desc")

    if task_desc :
        todo_service.add_note(task_desc)

    return redirect("/Todo")


@todo_bp.route("/Todo/Clear", methods=["POST"])
def clear():
    if request.method == "GET":
        return redirect("/Todo")

    tasks = todo_service.get_tasks()

    dataDone = tasks[ tasks['Status'] == 'Done'].reset_index().to_dict("records")

    for item in dataDone:
        todo_service.delete_task(item['Id'])

    return redirect("/Todo")




# for the dropdowns
@todo_bp.route("/Todo/update/<id>", methods=["POST", "GET"])
def updateTask(id):
    id=int(id)
    if request.method == "GET":
        return redirect("/Todo")

    new_status = request.form.get("Status")

    if new_status:
        todo_service.change_status(id, new_status)
        
    return redirect("/Todo")


# for the checkbox toggle:
@todo_bp.route("/Todo/toggle/<id>", methods=["POST", "GET"])
def toggleTask(id):
    id = int(id)
    if request.method == "GET":
        return redirect("/Todo")

    is_done = request.form.get("is_done")

    status = "Done" if is_done else "Pending"

    todo_service.change_status(id, status)
    return redirect("/Todo")
