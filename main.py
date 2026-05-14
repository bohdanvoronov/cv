from fastapi import FastAPI
from pydantic import BaseModel
import sqlite3
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
conn = sqlite3.connect('portfolio.db', check_same_thread=False)
cursor = conn.cursor()


cursor.execute('''
    CREATE TABLE IF NOT EXISTS messages (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        email TEXT,
        message TEXT
    )
''')
conn.commit()

# ---  Data Model ---
class ContactMessage(BaseModel):
    name: str
    email: str
    message: str



@app.get("/")
def read_root():
    return {"message": "Hello World! My CV API is running!"}

@app.get("/api/experience")
def get_experience():
    return {
        "company": "Carrier Global HVAC",
        "role": "Test Lead",
        "status": "Currently dominating testing here"
    }


@app.get("/api/messages")
def get_all_messages():

    cursor.execute("SELECT * FROM messages")
    rows = cursor.fetchall()
    
    saved_messages = []
    for row in rows:
        saved_messages.append({
            "id": row[0],
            "name": row[1],
            "email": row[2],
            "message": row[3]
        })
    return {"messages": saved_messages}


@app.post("/api/contact")
def send_message(msg: ContactMessage):
    
    cursor.execute('''
        INSERT INTO messages (name, email, message) 
        VALUES (?, ?, ?)
    ''', (msg.name, msg.email, msg.message))
    
    conn.commit() 
    
    return {"status": "success", "reply": f"Thanks {msg.name}, your message was saved to the database!"}