from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, Numeric
from database import Base
from typing import Optional


class WeatherZoneRequest(BaseModel):
    market: str
    dc: str
    congestionzone: str
    zip_code: str
    state: str
    load_profile: str = None

class VoltageRequest(BaseModel):
    market: str
    dc: str
    voltage: str

class VoltageResponse(BaseModel):
    market: str
    voltage: str
    

class Employee(BaseModel):
    emp_id: Optional[int]  # Auto-generated in DB
    emp_name: str
    department: str
    salary: float
    email: Optional[str] = None

class Config:
    from_attributes = True
   
    
class EmployeeDB(Base):
    __tablename__ = "employees"

    emp_id = Column(Integer, primary_key=True, index=True)
    emp_name = Column(String(100), nullable=False)
    department = Column(String(50), nullable=False)
    salary = Column(Numeric(10, 2), nullable=False)
    email = Column(String(100), unique=True)