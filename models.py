from pydantic import BaseModel
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
    emp_id: int
    emp_name: str
    department: str
    salary: float
    email: str = None