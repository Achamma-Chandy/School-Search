from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import Column, Integer, String

app = FastAPI()

# Database configuration
DATABASE_URL = "postgresql://postgres:<Password>@localhost/<dbname>"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Define the School model
class School(Base):
    __tablename__ = "schools"
    id = Column(Integer, primary_key=True, index=True)
    school_name = Column(String, index=True)
    address = Column(String)
    mrt_desc = Column(String)

# Templates configuration
templates = Jinja2Templates(directory="src/templates")

@app.get("/", response_class=HTMLResponse)
async def get_school_form(request: Request):
    return templates.TemplateResponse("school_form.html", {"request": request})

@app.post("/search", response_class=HTMLResponse)
async def search_school(request: Request, school_name: str = Form(...)):
    session = SessionLocal()
    try:
        query = select(School).where(School.school_name.ilike(f"%{school_name}%"))
        result = session.execute(query).scalars().all()
    finally:
        session.close()
    return templates.TemplateResponse("school_result.html", {"request": request, "schools": result})