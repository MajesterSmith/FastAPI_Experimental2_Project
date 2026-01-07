from fastapi import FastAPI,Request,HTTPException,Form,Depends
from fastapi.responses import HTMLResponse,RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
import database,re

app = FastAPI()
templates = Jinja2Templates(directory="templates")

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

def validate_user_data(email:str, password:str):
    email_regex = r'^\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    if not re.match(email_regex,email):
        return "Invalid email format"
    
    if len(password) < 8:
        return "Password must be at least 8 characters long"
    if not any(char.isdigit() for char in password):
        return "Password must contain at least one number."
    
    return None

@app.on_event("startup")
def create_admin():
    db = database.SessionLocal()
    admin_exists = db.query(database.UserInput).filter(database.UserInput.user_email == "admin@example.com").first()

    if not admin_exists:
        admin_user = database.UserInput(
            user_email = "admin@example.com",
            user_password = "password123"
        )
        db.add(admin_user)
        db.commit()
    db.close()

@app.get("/",response_class=HTMLResponse)
async def read_form(request: Request):
    return templates.TemplateResponse("home_page.html",{"request":request})

@app.get("/login_page", response_class=HTMLResponse)
async def login_form(request: Request):
    return templates.TemplateResponse("login_page.html", {"request": request})

@app.post("/submit")
async def handle_form(
    request: Request,    
    email: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    error_message = validate_user_data(email,password)

    if error_message:
        return templates.TemplateResponse("login_page.html",{"request" : request, "error" : error_message})

    user = db.query(database.UserInput).filter(
        database.UserInput.user_email == email,
        database.UserInput.user_password == password
    ).first()

    if user:
        return RedirectResponse(url = f"/display/{user.id}",status_code=303)
    else:
        return templates.TemplateResponse("login_page.html",{"request": request, "error" : "Invalid email or password"})

@app.get("/display/{item_id}", response_class=HTMLResponse)
async def display_string(request : Request, item_id : int, db: Session = Depends(get_db)):
    item = db.query(database.UserInput).filter(database.UserInput.id == item_id).first()
    return templates.TemplateResponse("result.html",{"request" : request, "text" : item.user_email})
