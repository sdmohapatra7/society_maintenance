# SocietyPro - Modern Housing Society Management System

SocietyPro is a comprehensive, full-stack management solution designed to automate the daily operations of residential and commercial societies. Built with a focus on automation, transparency, and high-fidelity user experience.

## 🚀 Core Features

### 🏢 Society & Asset Management
- **Multi-Society Support**: Manage multiple society wings or blocks under one dashboard.
- **House-wise Entry**: Detailed logging for every flat/shop including area square footage, wing details, and occupancy type.
- **Resident Directory**: Centralized database for resident names, contact details, and digital profiles.

### 💰 Automated Maintenance Billing
- **Dynamic Billing Engine**: Calculate maintenance based on fixed rates or square-footage-based charges.
- **XSLT Invoicing**: Generates professional, printable invoices using **XML to HTML (XSLT)** transformation for pixel-perfect presentation.
- **Monthly Automation**: Automatic generation of monthly bills for the entire society in one click.

### 📧 Smart Notifications
- **Email Integration**: Instant notification to residents as soon as an invoice is generated.
- **Date-Triggered Reminders**: An automated background worker (**APScheduler**) sends reminders 3 days before the due date to ensure timely collections.
- **Digital Receipts**: Instant confirmation for payments.

### 📊 PostgreSQL Analysis & Reporting
- **Financial Dashboard**: Real-time stats on "Total Collection" vs "Pending Dues" per society.
- **Billing Trends**: Visual charts showing historical collection patterns and target reaching.
- **Defaulter Tracking**: Quickly identify houses with overdue payments.

### 🔐 User Access Control (RBAC)
- **Multi-Role Support**: 
  - **Admin**: Full control over all societies, billing, and user management.
  - **Staff**: Manage billing tasks and resolve service requests/complaints.
  - **Resident (Member)**: Private portal to view personal invoices and file complaints.
- **Secure Authentication**: Password hashing and session management via **Flask-Login**.

### 🛠️ Complaint & Service Management
- **Digital Notice Board**: Admins can communicate with all residents instantly.
- **Resident Complaint System**: Residents can file plumbing, electrical, or security issues directly through their portal.
- **Resolution Tracking**: Admins can track resolution time and update status to keep residents informed.

### 🎨 Modern Tech Stack
| Layer | Technology |
|---|---|
| **Backend** | Python (Flask), SQLAlchemy |
| **Database** | PostgreSQL |
| **Frontend** | HTML5, Vanilla CSS (Premium Design), Bootstrap 5 (Login) |
| **Interactivity** | jQuery & AJAX (No page reloads) |
| **Reports** | XSLT / XML |
| **Tasks** | APScheduler / Flask-Mail |

## 🛠️ Installation & Setup

1. **Clone the project**
2. **Install requirements**:
   ```bash
   pip install -r requirements.txt
   ```
3. **Configure Database**:
   Update `DATABASE_URL` in `dev3/common/config.py`.
4. **Run the application**:
   ```bash
   python run.py
   ```

## 📝 Roadmap
- [ ] Payment Gateway Integration (Stripe/UPI).
- [ ] Mobile App for Security Guards.
- [ ] Amenity Booking for Clubhouses.

---
*Developed for Society Management Excellence.*