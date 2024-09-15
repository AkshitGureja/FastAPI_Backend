from pydantic import BaseModel, Field
from enum import Enum
from typing import Optional, List


class JobType(str, Enum):
    full_time = "full-time"
    part_time = "part-time"
    contract = "contract"


class JobCreate(BaseModel):
    job_title: str
    job_description: str
    skills_required: List[str]
    qualifications: str
    company_name: str
    location: str
    job_type: JobType
    salary: float


class JobUpdate(BaseModel):
    job_title: Optional[str]
    job_description: Optional[str]
    skills_required: Optional[List[str]]
    qualifications: Optional[str]
    company_name: Optional[str]
    location: Optional[str]
    job_type: Optional[JobType]
    salary: Optional[float]


class JobPartialUpdate(BaseModel):
    job_title: Optional[str] = None
    job_description: Optional[str] = None
    skills_required: Optional[List[str]] = None
    qualifications: Optional[str] = None
    company_name: Optional[str] = None
    location: Optional[str] = None
    job_type: Optional[JobType] = None
    salary: Optional[float] = None


class JobResponse(JobCreate):
    id: str


class UserCreate(BaseModel):
    username: str
    password: str
