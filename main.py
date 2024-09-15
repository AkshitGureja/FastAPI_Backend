from fastapi import FastAPI, Depends, HTTPException, status
from models import JobCreate, JobUpdate, JobResponse, UserCreate, JobPartialUpdate
from database import job_collection, user_collection
from bson import ObjectId
from auth import (
    authenticate_user,
    create_access_token,
    get_current_active_user,
    get_password_hash,
)
from fastapi.security import OAuth2PasswordRequestForm
from typing import List

app = FastAPI()


# User signup
@app.post("/signup")
async def create_user(user: UserCreate):
    existing_user = await user_collection.find_one({"username": user.username})
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")
    hashed_password = get_password_hash(user.password)
    await user_collection.insert_one(
        {"username": user.username, "password": hashed_password}
    )
    return {"msg": "User created successfully"}


# Token generation
@app.post("/token")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user["username"]})
    return {"access_token": access_token, "token_type": "bearer"}


# Create a job posting
@app.post("/jobs/", response_model=JobResponse)
async def create_job(
    job: JobCreate, current_user: UserCreate = Depends(get_current_active_user)
):
    job_id = await job_collection.insert_one(job.dict())
    return {**job.dict(), "id": str(job_id.inserted_id)}


# Get all job postings
@app.get("/jobs/", response_model=List[JobResponse])
async def get_jobs():
    jobs = await job_collection.find().to_list(1000)
    return [{**job, "id": str(job["_id"])} for job in jobs]


# Get a specific job by id
@app.get("/jobs/{job_id}", response_model=JobResponse)
async def get_job(job_id: str):
    job = await job_collection.find_one({"_id": ObjectId(job_id)})
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return {**job, "id": str(job["_id"])}


# Update an existing job posting
@app.put("/jobs/{job_id}", response_model=JobResponse)
async def update_job(
    job_id: str,
    job: JobUpdate,
    current_user: UserCreate = Depends(get_current_active_user),
):
    updated_job = {k: v for k, v in job.dict().items() if v is not None}
    if len(updated_job) >= 1:
        await job_collection.update_one(
            {"_id": ObjectId(job_id)}, {"$set": updated_job}
        )
    return {**updated_job, "id": job_id}


# Delete a job posting
@app.delete("/jobs/{job_id}")
async def delete_job(
    job_id: str, current_user: UserCreate = Depends(get_current_active_user)
):
    result = await job_collection.delete_one({"_id": ObjectId(job_id)})
    if result.deleted_count == 1:
        return {"msg": "Job deleted successfully"}
    raise HTTPException(status_code=404, detail="Job not found")


@app.patch("/jobs/{job_id}", response_model=JobResponse)
async def partial_update_job(
    job_id: str,
    job_update: JobPartialUpdate,
    current_user: UserCreate = Depends(get_current_active_user),
):
    update_data = {k: v for k, v in job_update.dict().items() if v is not None}
    if not update_data:
        raise HTTPException(status_code=400, detail="No fields to update")

    result = await job_collection.update_one(
        {"_id": ObjectId(job_id)}, {"$set": update_data}
    )

    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Job not found")

    updated_job = await job_collection.find_one({"_id": ObjectId(job_id)})
    return {**updated_job, "id": str(updated_job["_id"])}
