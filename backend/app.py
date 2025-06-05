from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import sqlite3
import json
from datetime import datetime
from typing import List, Optional
import random
import math

app = FastAPI(title="ECG Monitoring System")

# Database setup
DATABASE = 'health_monitor.db'

class Patient(BaseModel):
    name: str
    age: int
    gender: str

class ECGReading(BaseModel):
    patient_id: int
    reading_data: List[float]
    heart_rate: int

def init_db():
    """Initialize the database with required tables"""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS patients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            age INTEGER,
            gender TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS ecg_readings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_id INTEGER,
            reading_data TEXT,
            heart_rate INTEGER,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (patient_id) REFERENCES patients (id)
        )
    ''')
    
    conn.commit()
    conn.close()

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

@app.get("/")
async def root():
    return {"message": "ECG Monitoring System API", "status": "running"}

@app.post("/patients/")
async def create_patient(patient: Patient):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute(
        'INSERT INTO patients (name, age, gender) VALUES (?, ?, ?)',
        (patient.name, patient.age, patient.gender)
    )
    conn.commit()
    patient_id = cursor.lastrowid
    conn.close()
    
    return {"id": patient_id, "status": "created"}

@app.get("/patients/")
async def get_patients():
    conn = get_db_connection()
    patients = conn.execute('SELECT * FROM patients').fetchall()
    conn.close()
    
    return [dict(patient) for patient in patients]

@app.post("/ecg-reading/")
async def add_ecg_reading(reading: ECGReading):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute(
        'INSERT INTO ecg_readings (patient_id, reading_data, heart_rate) VALUES (?, ?, ?)',
        (reading.patient_id, json.dumps(reading.reading_data), reading.heart_rate)
    )
    conn.commit()
    reading_id = cursor.lastrowid
    conn.close()
    
    return {"id": reading_id, "status": "recorded"}

@app.get("/ecg-readings/{patient_id}")
async def get_ecg_readings(patient_id: int):
    conn = get_db_connection()
    readings = conn.execute(
        'SELECT * FROM ecg_readings WHERE patient_id = ? ORDER BY timestamp DESC',
        (patient_id,)
    ).fetchall()
    conn.close()
    
    return [dict(reading) for reading in readings]

@app.get("/live-ecg/")
async def get_live_ecg():
    """Generate simulated ECG data"""
    ecg_data = []
    
    # Generate realistic ECG waveform
    for i in range(200):
        t = i * 0.01  # 10ms intervals
        
        # P wave, QRS complex, T wave simulation
        if i % 60 < 10:  # QRS complex
            value = 100 + 50 * math.sin(i * 0.8) + random.uniform(-5, 5)
        elif i % 60 < 20:  # T wave
            value = 60 + 20 * math.sin(i * 0.3) + random.uniform(-3, 3)
        else:  # Baseline with P wave
            value = 50 + 10 * math.sin(i * 0.1) + random.uniform(-2, 2)
        
        ecg_data.append(round(value, 2))
    
    heart_rate = random.randint(65, 95)
    
    return {
        "ecg_data": ecg_data,
        "heart_rate": heart_rate,
        "timestamp": datetime.now().isoformat(),
        "status": "normal"
    }

@app.get("/system-status/")
async def system_status():
    return {
        "status": "online",
        "database": "connected",
        "sensors": "simulated",
        "uptime": datetime.now().isoformat()
    }

# Initialize database on startup
@app.on_event("startup")
async def startup_event():
    init_db()
    print("ECG Monitoring System started!")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)