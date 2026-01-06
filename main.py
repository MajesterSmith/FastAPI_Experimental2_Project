from fastapi import FastAPI,Request,Form
from fastapi.responses import HTMLResponse,RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
import database

app = FastAPI()
templates = Jinja2Templates(directory="templates")

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/",response_class=HTMLResponse)
async def read_form(request: Request):
    return templates.TemplateResponse("form.html",{"request":request})

@app.post("/submit")
async def handle_form(user_input: str = Form(...)):
    return RedirectResponse(url = f"/display?text={user_input}",status_code=303)

@app.get("/display")
async def display_string(request : Request, text: str):
    return templates.TemplateResponse("result.html",{"request":request, "text":text})