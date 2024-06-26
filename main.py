import datetime

from fastapi import FastAPI
from sqlalchemy import func
from sqlalchemy.orm import Session, selectinload

from database_connector import *

app = FastAPI()


@app.get('/employees')
def get_employees():
    with Session(autoflush=False, bind=engine) as db:
        emps = db.query(Employee).all()
        responce = []
        for i in emps:
            responce.append(i)

        return {'employees': responce}


@app.get('/categories')
def get_categories():
    with Session(autoflush=False, bind=engine) as db:
        categories = db.query(Category).all()
        responce = []
        for i in categories:
            responce.append(i)

        return {'categories': responce}


@app.get('/works')
def get_works():
    with Session(autoflush=False, bind=engine) as db:
        works = (
            db.query(Work)
            .options(selectinload(Work.employee))
            .all()
        )

        response = []
        for work in works:
            response.append({
                "id": work.id,
                "company_name": work.company_name,
                "date_of_work": work.date_of_work,
                "hours_worked": work.hours_worked,
                "employee_id": work.employee.id,
                "employee_full_name": work.employee.full_name
            })

        return {"works": response}


