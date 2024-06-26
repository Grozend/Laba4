from sqlalchemy import Column, Integer, String, Date, Float, ForeignKey, create_engine
from sqlalchemy.orm import relationship, DeclarativeBase

DATABASE_URL = "mysql://isp_p_Bliznykov:12345@77.91.86.135/isp_p_Bliznykov"
engine = create_engine(DATABASE_URL, echo=True)

class Base(DeclarativeBase): pass

class Employee(Base):
    __tablename__ = 'employee'

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(100), nullable=False)
    passport_number = Column(String(20), unique=True, nullable=False)
    date_of_birth = Column(Date, nullable=False)
    phone_number = Column(String(20), nullable=False)
    category_id = Column(Integer, ForeignKey('category.id'), nullable=False)

    category = relationship("Category", back_populates="employees")
    works = relationship("Work", back_populates="employee")

class Category(Base):
    __tablename__ = 'category'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, nullable=False)
    hourly_rate = Column(Float, nullable=False)

    employees = relationship("Employee", back_populates="category")

class Work(Base):
    __tablename__ = 'work'

    id = Column(Integer, primary_key=True, index=True)
    company_name = Column(String(100), nullable=False)
    employee_id = Column(Integer, ForeignKey('employee.id'), nullable=False)
    date_of_work = Column(Date, nullable=False)
    hours_worked = Column(Float, nullable=False)

    employee = relationship("Employee", back_populates="works")

Base.metadata.create_all(engine)