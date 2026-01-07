from fastapi import FastAPI,Request,Form,Depends
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
    return templates.TemplateResponse("home_page.html",{"request":request})

@app.get("/login_page", response_class=HTMLResponse)
async def login_form(request: Request):
    return templates.TemplateResponse("login_page.html", {"request": request})

@app.post("/submit")
async def handle_form(email: str = Form(...),
                  password: str = Form(...),
                  db: Session = Depends(get_db)
):
    new_entry = database.UserInput(
        user_email = email,
        user_password = password
    )
    db.add(new_entry)
    db.commit()
    db.refresh(new_entry)
    return RedirectResponse(url = f"/display/{new_entry.id}", status_code=303)


@app.get("/display/{item_id}", response_class=HTMLResponse)
async def display_string(request : Request, item_id : int, db: Session = Depends(get_db)):
    item = db.query(database.UserInput).filter(database.UserInput.id == item_id).first()
    return templates.TemplateResponse("result.html",{"request" : request, "text" : item.user_email})
