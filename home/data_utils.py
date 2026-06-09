import pandas as pd
import re
from django.db import transaction, IntegrityError
from django.core.exceptions import ValidationError
from .models import Student, Faculty

def parse_import_file(uploaded_file):
    """
    Parses a CSV or Excel file and returns a list of dictionaries representing clean rows.
    """
    name = uploaded_file.name.lower()
    
    try:
        if name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        elif name.endswith(('.xlsx', '.xls')):
            df = pd.read_excel(uploaded_file)
        else:
            raise ValidationError("Unsupported file format. Please upload a CSV (.csv) or Excel (.xlsx) file.")
    except Exception as e:
        raise ValidationError(f"Error reading spreadsheet file: {str(e)}")

    # Clean headers: strip whitespace, lowercase
    df.columns = [str(col).strip().lower().replace(' ', '_') for col in df.columns]
    
    # Fill NaN values with empty string
    df = df.fillna('')
    
    # Convert dataframe to list of dictionaries
    return df.to_dict(orient='records')

def validate_email(email):
    """Simple regex email validator"""
    if not email:
        return False
    return bool(re.match(r"[^@]+@[^@]+\.[^@]+", str(email).strip()))

def validate_phone(phone):
    """Verify phone consists of digits and is between 10-15 characters"""
    digits = re.sub(r"\D", "", str(phone))
    return len(digits) >= 10 and len(digits) <= 15

def import_students_from_list(rows):
    """
    Imports students from a list of dictionaries.
    Saves each row in a separate transactional block to import successful rows while reporting failed ones.
    """
    success_count = 0
    skipped_count = 0
    errors = [] # List of tuples: (row_num, error_message, row_data)

    # Standard columns mapping
    # Expected headers: name, roll_number, email, branch, year, phone, github_profile, dream_company, target_package, target_cgpa
    for idx, row in enumerate(rows, start=2): # Row 1 is header, data starts at row 2
        # Extrapolate keys safely (handling aliases/cases)
        name = str(row.get('name', row.get('student_name', ''))).strip()
        roll = str(row.get('roll_number', row.get('roll_no', row.get('roll', '')))).strip()
        email = str(row.get('email', row.get('email_address', ''))).strip()
        branch = str(row.get('branch', row.get('department', row.get('course', '')))).strip()
        year = str(row.get('year', row.get('academic_year', ''))).strip()
        phone = str(row.get('phone', row.get('phone_number', row.get('mobile', '')))).strip()
        
        # Twin fields
        github = str(row.get('github_profile', row.get('github', ''))).strip()
        dream_company = str(row.get('dream_company', row.get('target_company', 'Google'))).strip()
        
        try:
            target_package = float(row.get('target_package', row.get('package', 12.0)))
        except (ValueError, TypeError):
            target_package = 12.0
            
        try:
            target_cgpa = float(row.get('target_cgpa', row.get('cgpa', 8.5)))
        except (ValueError, TypeError):
            target_cgpa = 8.5

        # Row Data representation for reporting
        row_summary = f"Name: {name}, Roll: {roll}"

        # Validations
        row_errors = []
        if not name:
            row_errors.append("Name field is missing.")
        if not roll:
            row_errors.append("Roll Number field is missing.")
        if not email:
            row_errors.append("Email field is missing.")
        elif not validate_email(email):
            row_errors.append(f"Invalid email structure: '{email}'.")
        if not branch:
            row_errors.append("Branch field is missing.")
        if not year:
            row_errors.append("Year field is missing.")
        if not phone:
            row_errors.append("Phone number is missing.")
        elif not validate_phone(phone):
            row_errors.append(f"Invalid phone number length/characters: '{phone}'.")

        if row_errors:
            errors.append((idx, "; ".join(row_errors), row_summary))
            continue

        # Check for duplicates in DB
        if Student.objects.filter(roll_number=roll).exists():
            skipped_count += 1
            errors.append((idx, f"Duplicate Roll Number skipped: '{roll}' already exists.", row_summary))
            continue

        # Attempt transactional save for row
        try:
            with transaction.atomic():
                Student.objects.create(
                    name=name,
                    roll_number=roll,
                    email=email,
                    branch=branch,
                    year=year,
                    phone=phone,
                    github_profile=github if github else None,
                    dream_company=dream_company,
                    target_package=target_package,
                    target_cgpa=target_cgpa
                )
                success_count += 1
        except Exception as e:
            errors.append((idx, f"Database transaction failed: {str(e)}", row_summary))

    return {
        'success_count': success_count,
        'skipped_count': skipped_count,
        'errors': errors
    }

def import_faculty_from_list(rows):
    """
    Imports faculty members from a list of dictionaries.
    """
    success_count = 0
    skipped_count = 0
    errors = []

    # Expected: name, faculty_id, department, email, password
    for idx, row in enumerate(rows, start=2):
        name = str(row.get('name', row.get('faculty_name', ''))).strip()
        faculty_id = str(row.get('faculty_id', row.get('id', ''))).strip()
        department = str(row.get('department', row.get('dept', 'Computer Science'))).strip()
        email = str(row.get('email', ''))
        password = str(row.get('password', ''))

        row_summary = f"Name: {name}, ID: {faculty_id}"

        row_errors = []
        if not name:
            row_errors.append("Name field is missing.")
        if not faculty_id:
            row_errors.append("Faculty ID is missing.")
        if not password:
            row_errors.append("Default Password is missing.")

        if row_errors:
            errors.append((idx, "; ".join(row_errors), row_summary))
            continue

        # Check duplicate
        if Faculty.objects.filter(faculty_id=faculty_id).exists():
            skipped_count += 1
            errors.append((idx, f"Duplicate Faculty ID: '{faculty_id}' already registered.", row_summary))
            continue

        try:
            with transaction.atomic():
                Faculty.objects.create(
                    name=name,
                    faculty_id=faculty_id,
                    department=department,
                    password=password
                )
                success_count += 1
        except Exception as e:
            errors.append((idx, f"Database write failed: {str(e)}", row_summary))

    return {
        'success_count': success_count,
        'skipped_count': skipped_count,
        'errors': errors
    }
