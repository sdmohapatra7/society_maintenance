# 🏢 SocietyPro - Premium Society Management System

**SocietyPro** is a state-of-the-art, full-stack web application designed to streamline the administration and financial management of modern residential societies. It provides a seamless experience for administrators, staff, and residents alike.

---

## 🚀 Key Features

### 🔐 Advanced Security & Access Control
- **Role-Based Access Control (RBAC):** Dedicated interfaces for Admins, Staff, and Residents.
- **Dynamic Feature Management:** Admins can dynamically enable or disable specific modules (Billing, Complaints, Societies, etc.) for entire roles via a real-time dashboard.

### 💳 Financial & Billing Management
- **Automated Billing:** Generate maintenance bills based on fixed charges and area-based rates.
- **Razorpay Integration:** Secure online payment gateway for residents to pay bills instantly.
- **Professional PDF Invoices:** Automated generation of professional invoices with "PAID" verification stamps and payment dates.
- **Expense Tracking:** Comprehensive log of society expenditures with category-wise management.

### 🏠 Property & Resident Management
- **Society Hierarchy:** Manage multiple societies with their specific addresses and registration details.
- **House Management:** Track wings, house numbers, area square footage, and resident contact details.
- **User Management:** Secure registration and profile management for all community members.

### 🛠️ Resident Services
- **Complaint Helpdesk:** Residents can file complaints, upload documents, and track resolution status in real-time.
- **Announcements:** (Coming Soon) Digital notice board for society-wide communication.

### 🎨 Premium User Experience
- **Modern UI/UX:** Built with Bootstrap 5 and custom CSS for a clean, glassmorphism-inspired aesthetic.
- **Interactive Notifications:** Replaced generic browser popups with elegant Bootstrap Toasts and Confirmation Modals.
- **Smooth Animations:** Integrated CSS animations for a fluid feel during login and navigation.

---

## 🛠️ Technology Stack

- **Backend:** Python (Flask Framework)
- **Database:** PostgreSQL (Architected with SQLAlchemy & pg8000 for high compatibility)
- **Frontend:** HTML5, Vanilla CSS3, Bootstrap 5, jQuery
- **Payment Gateway:** Razorpay SDK
- **Reporting:** fpdf2 (for high-quality PDF generation)
- **Authentication:** Flask-Login

---

## 📂 Project Structure

```text
society_maintenance/
├── dev3/                   # Core Application Source
│   ├── bl/                 # Business Logic (Calculations, PDF logic)
│   ├── common/             # Config, DB Setup, & Auth Utilities
│   ├── handler/            # Flask Routes (Blueprints)
│   ├── sql/                # SQL Query Library & Schema
│   └── ui/                 # Frontend Assets
│       ├── static/         # CSS, JS (SocietyPro.js), & Images
│       └── templates/      # HTML Templates (Jinja2)
├── run.py                  # Application Entry Point
├── seed.py                 # Initial Database Seeding Script
└── requirements.txt        # Python Dependencies
```

---

## ⚙️ Installation & Setup

1. **Clone the repository** and navigate to the project root.
2. **Setup Virtual Environment:**
   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```
3. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
4. **Initialize Database:**
   Ensure PostgreSQL is running, then seed the initial data:
   ```bash
   python seed.py
   ```
5. **Run the Application:**
   ```bash
   python run.py
   ```
   Access the app at `http://127.0.0.1:5000`

---

## 👨‍💻 Contributing
This project is architected for scalability. To add a new feature:
1. Define the SQL in `dev3/sql/`.
2. Implement Business Logic in `dev3/bl/`.
3. Create a Route Handler in `dev3/handler/`.
4. Register the Blueprint in `dev3/__init__.py`.