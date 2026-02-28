from fastapi import FastAPI, Depends, Request, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.category import Category
from app.models.question import Question, QuestionType
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from typing import List, Optional
import uuid

app = FastAPI()

templates = Jinja2Templates(directory="app/static/question")


class QuestionIn(BaseModel):
    question: str
    type: str
    options: Optional[List[str]] = None
    answer: str


class CategoryIn(BaseModel):
    name: str
    questions: List[QuestionIn]


@app.get("/")
def serve_categories(request: Request, db: Session = Depends(get_db)):
    categories = db.query(Category).all()
    return templates.TemplateResponse("categories.html", {"request": request, "categories": categories})


@app.get("/admin/create")
def serve_admin(request: Request):
    return templates.TemplateResponse("admin.html", {"request": request})


@app.post("/admin/create")
def create_category(payload: CategoryIn, db: Session = Depends(get_db)):
    existing = db.query(Category).filter(Category.name == payload.name).first()
    if existing:
        raise HTTPException(status_code=400, detail="Category already exists")

    category = Category(id=uuid.uuid4(), name=payload.name)
    db.add(category)
    db.commit()
    db.refresh(category)

    for q in payload.questions:
        question = Question(
            id=uuid.uuid4(),
            question=q.question,
            type=QuestionType(q.type),
            options=q.options,
            answer=q.answer,
            category_id=category.id
        )
        db.add(question)

    db.commit()
    return JSONResponse({"status": "ok", "category": payload.name})


@app.get("/{category}")
def serve_quiz(request: Request, category: str, db: Session = Depends(get_db)):
    questions = (
        db.query(Question)
        .join(Category, Question.category_id == Category.id)
        .filter(Category.name == category)
        .all()
    )
    questions_data = [
        {
            "question": q.question,
            "type": q.type.value,
            "options": q.options or [],
            "answer": q.answer
        }
        for q in questions
    ]
    return templates.TemplateResponse("index.html", {"request": request, "questions": questions_data})