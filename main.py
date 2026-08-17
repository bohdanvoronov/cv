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

class ContactMessage(BaseModel):
    name: str
    email: str
    message: str

@app.get("/")
def read_root():
    return {"message": "Hello World! My CV API is running!"}

@app.get("/api/about")
def get_about_me():
    return {
        "title": "QA Engineer / Test Lead",
        "experience": "6 years of commercial experience",
        "bio": "QA Engineer / Test Lead with 6 years of commercial experience. I am passionate about testing and delivering high-quality products. Always eager to learn new skills and technologies, and to collaborate with diverse and talented teams. Motivated by challenging and innovative projects that require problem-solving, creativity, and attention to detail. My goal is to improve your product quality and save your money.",
        "languages": ["English — C1", "Czech — B2", "Ukrainian — Native", "Russian — Fluent"]
    }

@app.get("/api/experience")
def get_experience():
    return {
        "experiences": [
            {
                "role": "Adobe QA Developer / Test Lead",
                "company": "Carrier Global HVAC",
                "period": "Aug 2025 - Present",
                "location": "Prague, Czechia · Hybrid",
                "highlights": [
                    "Design and execute complex testing flows across Adobe Experience Manager (AEM) and integrated platforms.",
                    "Solr & Search Testing: Designed QA strategies for Solr search logic, indexing validation, and multilingual edge cases.",
                    "Performance Testing: Conducted UI performance testing using Lighthouse CLI (Core Web Vitals) and load/stress testing using JMeter.",
                    "AEM Testing & Validation: Author and validate components in AEM editor, test Brightcove video integrations and SEO elements.",
                    "QA Leadership: Sole QA for regression and functional verification, and mentor a team of 3 QA engineers."
                ]
            },
            {
                "role": "Automation Quality Assurance Engineer",
                "company": "Publicis Groupe (Pfizer Project)",
                "period": "Sep 2023 - Aug 2025",
                "location": "Prague, Czechia · Hybrid",
                "highlights": [
                    "Developed automated test suites from scratch using Python, Selenium, and Requests library covering 70% of API endpoints.",
                    "Integrated automated test cases into CI/CD pipelines using GitLab.",
                    "Performed functional, exploratory, and cross-browser testing across web, mobile (iOS/Android), and tools like Xcode, Veeva CRM.",
                    "Led backend testing tasks, validating data integrity with MySQL and RESTful APIs.",
                    "Mentored 5 Test Engineers and advanced their technical skills."
                ]
            },
            {
                "role": "Automation QA Engineer",
                "company": "Linguamat.com, s.r.o. (Social Media Platform)",
                "period": "Dec 2022 - Sep 2023",
                "location": "Prague, Czechia · Hybrid",
                "highlights": [
                    "Developed and maintained robust automation test scripts using Python, Selenium, and requests for regression and smoke tests.",
                    "Achieved 60%+ test coverage through automation, reducing manual testing effort.",
                    "Integrated automated test suites into CI/CD pipeline using GitHub Actions.",
                    "Conducted database testing using MySQL and performance load scenarios."
                ]
            },
            {
                "role": "General QA Engineer",
                "company": "NIX Solutions (Cengage Learning)",
                "period": "Nov 2021 - Jan 2023",
                "location": "Kharkiv, Ukraine · Hybrid",
                "highlights": [
                    "Developed automation scripts using Python and Selenium for product search, checkout, and authentication.",
                    "Performed API endpoint testing with Postman and database testing using MySQL.",
                    "Monitored and improved performance and load testing scenarios."
                ]
            },
            {
                "role": "Junior QA Engineer / Trainee / Intern",
                "company": "Magnise (Wehkamp Market Place)",
                "period": "Dec 2020 - Nov 2021",
                "location": "Hybrid",
                "highlights": [
                    "Conducted manual and automated testing for web and mobile applications.",
                    "Utilized JIRA for bug tracking and TestRail for test case management.",
                    "Assisted in basic API testing using Postman and database verification using MySQL."
                ]
            }
        ]
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