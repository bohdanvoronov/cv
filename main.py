from fastapi import FastAPI
from fastapi.responses import FileResponse
from pydantic import BaseModel
import sqlite3
from fastapi.middleware.cors import CORSMiddleware
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

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

def send_email_notification(name, sender_email_user, user_message):
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    
    # PUT YOUR GMAIL AND 16-CHAR APP PASSWORD HERE:
    my_gmail = "YOUR_EMAIL@gmail.com"
    my_app_password = "YOUR_16_CHAR_APP_PASSWORD"

    msg = MIMEMultipart()
    msg['From'] = my_gmail
    msg['To'] = my_gmail
    msg['Subject'] = f"🚀 New Portfolio Message from {name}"

    body = f"""
    You have received a new message from your portfolio contact form!

    Name: {name}
    Email: {sender_email_user}
    
    Message:
    {user_message}
    """
    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(my_gmail, my_app_password)
        server.sendmail(my_gmail, my_gmail, msg.as_string())
        server.quit()
    except Exception as e:
        print(f"Error sending email: {e}")

@app.get("/")
def read_root():
    return FileResponse("index.html")

@app.get("/profile.JPG")
def get_profile_image():
    return FileResponse("profile.JPG")

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
                    "As dedicated QA Lead, design, execute, and validate complex testing flows across Adobe Experience Manager (AEM) and integrated platforms, combining hands-on testing with team mentorship and release risk management.",
                    "QA Leadership & Process Improvement: Serve as sole QA Lead for end-to-end regression, functional, and metadata validation across frontend and backend applications.",
                    "Mentor a team of 3 QA engineers (1 Senior, 2 Juniors) on testing strategies, execution tools, and standardized bug reporting.",
                    "Partner with Product Owners, Developers, and Content Authors to clarify edge-case requirements and document reusable QA checklists and test plans.",
                    "AEM & Content Authoring Validation: Test and author complex AEM components (such as 50/50 layout components, Asset/CTA tabs, and background color toggles) across editor.html and wcmmode=disabled authoring environments.",
                    "Validate Brightcove video integrations (inline players and modal overlay behaviors) across responsive layouts.",
                    "CDN, Edge Routing & SEO Testing: Validate CDN (Fastly/Adobe Cloud) and Dispatcher rewrite rules, verifying trailing slash standardization, canonical tags, and hreflang.",
                    "Ensure edge delivery compliance by preventing unwanted external domain redirects (such as pagescdn.com host routing).",
                    "Perform technical SEO verifications, ensuring meta tags, indexation rules, and structured data match release specifications.",
                    "Search & Solr Engine QA: Design QA strategies for Solr search logic, including indexing validation, timestamp mapping, and multilingual search edge cases.",
                    "Deliver live technical demos to non-technical stakeholders showcasing validation results and technical risks.",
                    "Performance, Automation & Cross-Browser Testing: Automate Lighthouse CLI performance checks (measuring Core Web Vitals like FCP, LCP, and CLS) using custom Bash scripts.",
                    "Perform API load and stress testing using Apache JMeter to validate backend stability.",
                    "Execute cross-browser and cross-device testing across Chrome, Firefox, Safari, and Edge on desktop, tablet, and mobile via BrowserStack Live and BrowserStack Local tunnels."
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

# @app.post("/api/contact")
# def send_message(msg: ContactMessage):
#     cursor.execute('''
#         INSERT INTO messages (name, email, message) 
#         VALUES (?, ?, ?)
#     ''', (msg.name, msg.email, msg.message))
#     conn.commit()
#     return {"status": "success", "reply": f"Thanks {msg.name}, your message was saved to the database!"}


@app.post("/api/contact")
def send_message(msg: ContactMessage):
    # 1. Save to SQLite Database
    cursor.execute('''
        INSERT INTO messages (name, email, message) 
        VALUES (?, ?, ?)
    ''', (msg.name, msg.email, msg.message))
    conn.commit()
    
    # 2. Send email notification to your Gmail
    send_email_notification(msg.name, msg.email, msg.message)

    return {"status": "success", "reply": f"Thanks {msg.name}, your message was saved to the database and emailed!"}
