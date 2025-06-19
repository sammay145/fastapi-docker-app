from fastapi import FastAPI, Request, Form
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()

# In-memory task list
tasks = []

# Mount static files (CSS)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Set up Jinja2 templates
templates = Jinja2Templates(directory="templates")

@app.get("/")
def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "tasks": tasks})

@app.post("/add")
def add_task(task: str = Form(...)):
    tasks.append(task)
    return RedirectResponse("/", status_code=303)

@app.post("/delete")
def delete_task(task_index: int = Form(...)):
    if 0 <= task_index < len(tasks):
        tasks.pop(task_index)
    return RedirectResponse("/", status_code=303)
