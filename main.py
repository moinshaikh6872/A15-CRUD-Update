from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List

app = FastAPI(title="CRUD API - Create, Read, Update")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Models for data validation
class RecordUpdate(BaseModel):
    title: str
    details: str

class Record(RecordUpdate):
    id: int

# In-memory database and ID tracker
database = []
current_id = 1

@app.get("/records", response_model=List[Record])
def read_records():
    """Reads and returns all stored records."""
    return database

@app.post("/records", response_model=Record)
def create_record(record_in: RecordUpdate):
    """Creates a new record with an auto-incrementing ID."""
    global current_id
    new_record = Record(id=current_id, title=record_in.title, details=record_in.details)
    database.append(new_record)
    current_id += 1
    return new_record

@app.put("/records/{record_id}", response_model=Record)
def update_record(record_id: int, record_in: RecordUpdate):
    """Updates an existing record by ID."""
    for record in database:
        if record.id == record_id:
            record.title = record_in.title
            record.details = record_in.details
            return record
    raise HTTPException(status_code=404, detail="Record not found")
