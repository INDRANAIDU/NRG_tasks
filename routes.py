from fastapi import APIRouter
from models import WeatherZoneRequest, VoltageRequest, VoltageResponse, Employee
from voltage import translate_voltage
from weatherzone import translate_weatherzone
from get_weatherzone import get_weatherzone
import csv
from typing import Dict, List
from fastapi import HTTPException


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



employees = []  

@router.post("/employees/")
def add_employees(new_employees: List[Employee]):
    try:
        for employee in new_employees:
  
            if any(existing.id == employee.id for existing in employees):
                raise HTTPException(status_code=400, detail=f"Employee with ID {employee.id} already exists")
            employees.append(employee)
        return {"message": "Employees added successfully", "employees": employees}
    except HTTPException as e:
        raise e



@router.get("/employees/")
def get_all_employees():
    try:
        return employees
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/employees/{employee_id}")
def get_employee(employee_id: int):
    try:
        if employee_id not in [emp.id for emp in employees]:
            raise HTTPException(status_code=404, detail="Employee not found")
        return next(emp for emp in employees if emp.id == employee_id)
    except HTTPException as e:
        raise e


@router.delete("/employees/{employee_id}")
def delete_employee(employee_id: int):
    try:
        for i, emp in enumerate(employees):
            if emp.id == employee_id:
                del employees[i]   
                return {"message": "Employee deleted successfully"}
            raise HTTPException(status_code=404, detail="Employee not found")   
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/employees/{employee_id}")
def update_employee(employee_id: int, employee: Employee):
    try:
        for i, emp in enumerate(employees):
            if emp.id == employee_id:
                employees[i] = employee
                return {"message": "Employee updated successfully", "employee": employee}
        raise HTTPException(status_code=404, detail="Employee not found")
    except HTTPException as e:
        raise e

    
