# College ERP Management System

A production-quality Django-based College ERP and AI Digital Twin Management System. It features Student and Faculty portals, Attendance/Marks tracking, Timetable scheduling, Announcement notifications, and Data Management capabilities.

---

## 🚀 Quick Start

### 1. Prerequisites
Ensure you have **Python 3.10+** installed.

### 2. Setup Environment & Install Dependencies
Run the following commands in your terminal:

```bash
# Create a virtual environment
python -m venv .venv

# Activate the virtual environment
# On Windows:
.venv\Scripts\activate
# On macOS/Linux:
source .venv/bin/activate

# Install requirements
pip install -r requirements.txt
```

### 3. Run Migrations & Start Server
```bash
# Apply database migrations
python manage.py migrate

# Start the development server
python manage.py runserver
```
Visit the app in your browser at `http://127.0.0.1:8000/`.

---

## 🛠️ Key Features

### 👨‍🎓 Student Portal
- **Dashboard & Profile:** Access personal details, academic metrics, and assignment progress.
- **AI Digital Twin:** Tracks study habits, coding metrics, stress levels, dream companies, and package targets.

### 👩‍🏫 Faculty Portal
- **Attendance & Marks:** Update student subject attendance and exams/marks.
- **Academic Setup:** Upload announcements (notices) and lecture timetables.

### 📊 Data Management Portal
- **Bulk Imports:** Populate students or faculty details dynamically from CSV or Excel sheets.
- **Sample Sheets:**
  - Student Sample CSV: [students_test.csv](file:///c:/PROJECTS/COLLEGE_ERP/students_test.csv)
  - Student Sample Excel: [students_test.xlsx](file:///c:/PROJECTS/COLLEGE_ERP/students_test.xlsx)
  - Faculty Sample Excel: [faculty_test.xlsx](file:///c:/PROJECTS/COLLEGE_ERP/faculty_test.xlsx)

---

## 📁 Project Structure

- `core/` - Main Django settings, configuration, and URL routers.
- `home/` - Main app containing views, models, forms, templates, and import utilities.
  - [models.py](file:///c:/PROJECTS/COLLEGE_ERP/home/models.py) - Defines Student, Faculty, Attendance, Marks, Notice, and Timetable models.
  - [views.py](file:///c:/PROJECTS/COLLEGE_ERP/home/views.py) - Handles the business logic for logins, dashboards, data imports, and searching.
  - [forms.py](file:///c:/PROJECTS/COLLEGE_ERP/home/forms.py) - Form validations for student registrations and profile updates.
  - [data_utils.py](file:///c:/PROJECTS/COLLEGE_ERP/home/data_utils.py) - Helper scripts for processing bulk uploads.
