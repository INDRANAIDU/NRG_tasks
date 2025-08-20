from fastapi import APIRouter
from models import WeatherZoneRequest, VoltageRequest, VoltageResponse, Employee, EmployeeDB
from voltage import translate_voltage
from weatherzone import translate_weatherzone
from get_weatherzone import get_weatherzone
import csv
from typing import Dict, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from database import SessionLocal


router = APIRouter()

@router.get("/translate_voltage/{market}/{dc}/{voltage}")
def translate_voltage_endpoint(market: str, dc: str, voltage: str):
    try:
        translated_voltage = translate_voltage(market, dc, voltage)
        return VoltageResponse(market=market, voltage=translated_voltage)
    except Exception as e:
        return {"error": str(e)}

@router.get("/get_weatherzone/{market}/{dc}/{congestionzone}/{zip_code}")
def get_weatherzone_endpoint(
    market: str,
    dc: str,
    congestionzone: str,
    zip_code: str,
    state: str,
    load_profile: str = None
):
    try:
        weatherzone = get_weatherzone(
            market,
            dc,
            congestionzone,
            zip_code,
            state,
            load_profile
        )
        return {"weatherzone": weatherzone}
    except Exception as e:
        raise {"error": str(e)}

@router.get("/translate_weatherzone/{market}/{congestionzone}")
def translate_weatherzone_endpoint(market: str, congestionzone: str):
    try: 
        translated_weatherzone = translate_weatherzone(market, congestionzone)
        return {"translated_weatherzone": translated_weatherzone}
    except Exception as e:
        return {"error": str(e)}


@router.post("/new/")
def add_voltage_entry(
    market: str, 
    old_weatherzone: str, 
    new_weatherzone: str = None
    ):
    try:
        with open("translate_weatherzone.csv", mode="a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([market, old_weatherzone, new_weatherzone])

        return {"message": "New entry added successfully"}
    except Exception as e:
        return {"error": str(e)}


async def get_db():
    async with SessionLocal() as session:
        yield session


@router.post("/employees/")
async def add_employee(employee: Employee, db: AsyncSession = Depends(get_db)):
    db_employee = EmployeeDB(
        emp_id=employee.emp_id,
        emp_name=employee.emp_name,
        department=employee.department,
        salary=employee.salary,
        email=employee.email,
    )
    db.add(db_employee)
    await db.commit()
    await db.refresh(db_employee)
    return db_employee


@router.get("/employees/")
async def get_all_employees(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(EmployeeDB))
    employees = result.scalars().all()
    return employees


@router.get("/employees/{employee_id}")
async def get_employee(employee_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(EmployeeDB).where(EmployeeDB.emp_id == employee_id))
    employee = result.scalar_one_or_none()
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    return employee


@router.put("/employees/{employee_id}")
async def update_employee(employee_id: int, updated_employee: Employee, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(EmployeeDB).where(EmployeeDB.emp_id == employee_id))
    employee = result.scalar_one_or_none()
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")

    employee.emp_name = updated_employee.emp_name
    employee.department = updated_employee.department
    employee.salary = updated_employee.salary
    employee.email = updated_employee.email

    await db.commit()
    await db.refresh(employee)
    return employee


@router.delete("/employees/{employee_id}")
async def delete_employee(employee_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(EmployeeDB).where(EmployeeDB.emp_id == employee_id))
    employee = result.scalar_one_or_none()
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")

    await db.delete(employee)
    await db.commit()
    return {"message": "Employee deleted successfully"}