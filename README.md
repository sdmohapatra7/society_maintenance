🏢 Society Maintenance Management System

A web-based Society Maintenance Management System built with Flask + PostgreSQL + SQLAlchemy.
This project helps manage users, bills, complaints, and events in a housing society, with a simple UI and external service integrations (Email, WhatsApp).

✨ Features

🔑 User Authentication (login, sessions)

📄 Bill Management (generate, track, update payment status)

🛠️ Complaint Tracking (submit, view, resolve complaints)

📅 Event Management (create and list community events)

📧 Email Notifications (via email_service)

📱 WhatsApp Notifications (via whatsapp_service)

🎨 UI with HTML, CSS, JS, XSLT

📂 Project Structure
society_maintenance/
│── run.py                 # Application entry point
│── requirements.txt       # Dependencies
│
│── dev3/
│   ├── common/            # Config & DB connection
│   ├── models/            # Database models
│   ├── bl/                # Business Logic
│   ├── handlers/          # Routes / Controllers
│   ├── services/          # External integrations
│   └── ui/                # Templates & Static files
│

⚙️ Installation & Setup
1️⃣ Clone the Repository
git clone https://github.com/<your-username>/society_maintenance.git
cd society_maintenance

2️⃣ Create Virtual Environment
python -m venv venv
source venv/bin/activate   # On Linux/Mac
venv\Scripts\activate      # On Windows

3️⃣ Install Dependencies
pip install -r requirements.txt

4️⃣ Configure Environment Variables

Create a .env file in root:

FLASK_SECRET=supersecretkey
DATABASE_URL=postgresql+psycopg2://username:password@localhost:5432/society_db


Replace username, password, and society_db with your PostgreSQL details.

5️⃣ Initialize Database
flask --app run.py db init
flask --app run.py db migrate -m "Initial tables"
flask --app run.py db upgrade

6️⃣ Run the Application
python run.py


Visit: 👉 http://127.0.0.1:5000

📸 Screenshots (optional)

(Add later once your UI is ready — login page, dashboard, bills, etc.)

🚀 Future Improvements

✅ Role-based access (Admin / User)

✅ Online payment gateway integration

✅ Push notifications

✅ Mobile app (React Native / Flutter)

🤝 Contributing

Pull requests are welcome! For major changes, please open an issue first to discuss what you’d like to change.

📜 License

This project is licensed under the MIT License.