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


@app.get('/ordered_employees')
def get_employees():
    with Session(autoflush=False, bind=engine) as db:
        emps = db.query(Employee).order_by(Employee.full_name).all()
        responce = []
        for i in emps:
            responce.append(i)

        return {'employees': responce}


@app.get('/ordered_categories')
def get_categories():
    with Session(autoflush=False, bind=engine) as db:
        categories = db.query(Category).order_by(Category.hourly_rate).all()
        responce = []
        for i in categories:
            responce.append(i)

        return {'categories': responce}


@app.get('/ordered_works')
def get_works():
    with Session(autoflush=False, bind=engine) as db:
        works = (
            db.query(Work)
            .options(selectinload(Work.employee))
            .order_by(Work.date_of_work)
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


@app.get('/employees/categories/1-2')
def get_employees_by_categories():
    with Session(autoflush=False, bind=engine) as db:
        employees = db.query(Employee).filter(Employee.category_id.in_([2, 3])).all()
        return {"employees": employees}


@app.get('/works/hours_more_10')
def get_works_hours_gt_10():
    with Session(autoflush=False, bind=engine) as db:
        works = db.query(Work).filter(Work.hours_worked > 10).all()
        return {"works": works}


@app.get('/employees/hours_by_work')
def get_employees_hours_by_work():
    with Session(autoflush=False, bind=engine) as db:
        result = db.query(Employee, func.sum(Work.hours_worked).label('total_hours')).join(Work,
                                                                                           Work.employee_id == Employee.id).group_by(
            Employee.id).all()
        return {"result": result}


@app.get('/works/total_cost')
def get_works_total_cost():
    with Session(autoflush=False, bind=engine) as db:
        result = db.query(func.sum(Work.hours_worked * Employee.category.hourly_rate)).join(Employee).scalar()
        return {"total_cost": result}


@app.get('/employees/seniority_gt_5')
def get_employees_seniority_gt_5():
    with Session(autoflush=False, bind=engine) as db:
        five_years_ago = datetime.date.today() - datetime.timedelta(days=5 * 365)
        employees = db.query(Employee).filter(
            datetime.date.today() - Employee.date_of_employment > datetime.timedelta(days=5 * 365)).all()
        return {"employees": employees}


@app.get('/employees/by_category')
def get_employees_by_category():
    with Session(autoflush=False, bind=engine) as db:
        employees = db.query(Employee).join(Category).order_by(Employee.full_name).all()
        return {"employees": employees}


@app.get('/works/by_employee_and_date')
def get_works_by_employee_and_date():
    with Session(autoflush=False, bind=engine) as db:
        works = db.query(Work, Employee.full_name).join(Employee, Work.employee_id == Employee.id).order_by(
            Work.date_of_work).all()
        return {"works": works}


@app.get('/categories/employees_count_gt_1_year')
def get_categories_employees_count_gt_1_year():
    with Session(autoflush=False, bind=engine) as db:
        one_year_ago = datetime.date.today() - datetime.timedelta(days=365)
        categories = db.query(Category, func.count(Employee.id).label('employee_count')).join(Employee).filter(
            Employee.date_of_employment < one_year_ago).group_by(Category.id).order_by(Category.id).all()
        return {"categories": categories}


@app.get('/employees/total_cost_by_employee')
def get_employees_total_cost_by_employee():
    with Session(autoflush=False, bind=engine) as db:
        result = db.query(Employee,
                          func.sum(Work.hours_worked * Employee.category.hourly_rate).label('total_cost')).join(Work,
                                                                                                                Work.employee_id == Employee.id).group_by(
            Employee.id).all()
        return {"result": result}


@app.post('/employee/new')
def new_employee(full_name: str,
                 passport_number: str,
                 date_of_birth: datetime.date,
                 phone_number: str,
                 category_id: int):
    new_emp = Employee(full_name=full_name,
                       passport_number=passport_number,
                       date_of_birth=date_of_birth,
                       phone_number=phone_number,
                       category_id=category_id)
    try:
        with Session(autoflush=False, bind=engine) as db:
            db.add(new_emp)
            db.commit()
            db.refresh(new_emp)
        return {'message': 'успешно добавлен', 'new_employee': new_emp}
    except Exception as e:
        return {'Fatal Error': e}


@app.post('/works/new')
def new_work(comp_name: str,
             emp_id: int,
             date: str,
             hour: int):
    new_work = Work(company_name=comp_name, employee_id=emp_id, date_of_work=date, hours_worked=hour)
    with Session(autoflush=False, bind=engine) as db:
        db.add(new_work)
        db.commit()
        db.refresh(new_work)

    return new_work

@app.post('/category/new')
def new_category(name:str, rate:float):
    new_category = Category(name=name, hourly_rate=rate)
    with Session(autoflush=False, bind=engine) as db:
        db.add(new_category)
        db.commit()
        db.refresh(new_category)
    return new_category