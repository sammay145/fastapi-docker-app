from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()

# Updated: each task is a dict with 'name' and 'done'
tasks = []

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/")
def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "tasks": tasks})

@app.post("/add")
def add_task(task: str = Form(...)):
    tasks.append({"name": task, "done": False})
    return RedirectResponse("/", status_code=303)

@app.post("/delete")
def delete_task(task_index: int = Form(...)):
    if 0 <= task_index < len(tasks):
        tasks.pop(task_index)
    return RedirectResponse("/", status_code=303)

@app.post("/update")
def update_task(task_index: int = Form(...), new_task: str = Form(...)):
    if 0 <= task_index < len(tasks):
        tasks[task_index]["name"] = new_task
    return RedirectResponse("/", status_code=303)

@app.post("/toggle")
def toggle_task_done(task_index: int = Form(...)):
    if 0 <= task_index < len(tasks):
        tasks[task_index]["done"] = not tasks[task_index]["done"]
    return RedirectResponse("/", status_code=303)

@app.post("/clear")
def clear_tasks():
    tasks.clear()
    return RedirectResponse("/", status_code=303)

@app.get("/tasks")
def list_tasks():
    return {"tasks": tasks}

@app.get("/task/{task_index}")
def get_task(task_index: int):
    if 0 <= task_index < len(tasks):
        return tasks[task_index]
    else:
        raise HTTPException(status_code=404, detail="Task not found")
