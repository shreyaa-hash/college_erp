from django.shortcuts import render, redirect
from datetime import date
from django.core.exceptions import ValidationError
from .models import Student, Faculty, Attendance, Marks, Notice, Timetable
from .forms import (
    StudentRegistrationForm, StudentProfileForm, 
    AttendanceForm, MarksForm, TimetableForm, NoticeForm,
    BulkUploadForm
)
from .data_utils import (
    parse_import_file, import_students_from_list, import_faculty_from_list
)

def home(request):
    return render(request, 'home.html')

def login(request):
    message = ""
    if request.method == "POST":
        roll = request.POST.get('roll_number')
        try:
            student = Student.objects.get(roll_number=roll)
            request.session['student_roll'] = student.roll_number
            request.session['student_name'] = student.name
            return redirect('dashboard')
        except Student.DoesNotExist:
            message = "Invalid Roll Number"
    return render(request, 'login.html', {'message': message})

def dashboard(request):
    student_roll = request.session.get('student_roll')
    if not student_roll:
        return redirect('login')
    
    try:
        student = Student.objects.get(roll_number=student_roll)
    except Student.DoesNotExist:
        request.session.flush()
        return redirect('login')
        
    attendance = Attendance.objects.filter(student=student)
    notices = Notice.objects.all().order_by('-id')[:5]  # Latest 5 notices
    timetable = Timetable.objects.all()
    marks = Marks.objects.filter(student=student)

    # Marks Analytics
    total_marks = 0
    total_max_marks = 0
    for mark in marks:
        total_marks += mark.marks
        total_max_marks += mark.total_marks

    percentage = (total_marks / total_max_marks * 100) if total_max_marks > 0 else 0
    cgpa = round(percentage / 10, 2)

    # Attendance Analytics
    present_count = attendance.filter(status="Present").count()
    absent_count = attendance.filter(status="Absent").count()
    total_classes = attendance.count()
    attendance_percentage = (
        (present_count / total_classes) * 100
        if total_classes > 0 else 0
    )

    return render(request, 'dashboard.html', {
        'student': student,
        'attendance': attendance,
        'notices': notices,
        'timetable': timetable,
        'marks': marks,
        'total_marks': total_marks,
        'total_max_marks': total_max_marks,
        'percentage': round(percentage, 2),
        'cgpa': cgpa,
        'present_count': present_count,
        'absent_count': absent_count,
        'attendance_percentage': round(attendance_percentage, 2),
    })

def profile(request):
    student_roll = request.session.get('student_roll')
    if not student_roll:
        return redirect('login')
        
    try:
        student = Student.objects.get(roll_number=student_roll)
    except Student.DoesNotExist:
        request.session.flush()
        return redirect('login')
        
    return render(request, 'profile.html', {'student': student})

def edit_profile(request):
    student_roll = request.session.get('student_roll')
    if not student_roll:
        return redirect('login')
        
    try:
        student = Student.objects.get(roll_number=student_roll)
    except Student.DoesNotExist:
        request.session.flush()
        return redirect('login')

    if request.method == "POST":
        form = StudentProfileForm(request.POST, request.FILES, instance=student)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = StudentProfileForm(instance=student)

    return render(request, 'edit_profile.html', {'form': form, 'student': student})

def logout(request):
    request.session.flush()
    return redirect('home')

def faculty_login(request):
    message = ""
    if request.method == "POST":
        faculty_id = request.POST.get('faculty_id')
        password = request.POST.get('password')
        try:
            faculty = Faculty.objects.get(faculty_id=faculty_id, password=password)
            request.session['faculty_id'] = faculty.faculty_id
            request.session['faculty_name'] = faculty.name
            return redirect('faculty_dashboard')
        except Faculty.DoesNotExist:
            message = "Invalid Credentials"
    return render(request, 'faculty_login.html', {'message': message})

def faculty_dashboard(request):
    faculty_id = request.session.get('faculty_id')
    if not faculty_id:
        return redirect('faculty_login')
    
    try:
        faculty = Faculty.objects.get(faculty_id=faculty_id)
    except Faculty.DoesNotExist:
        request.session.flush()
        return redirect('faculty_login')

    students_count = Student.objects.count()
    notices_count = Notice.objects.count()
    timetable_count = Timetable.objects.count()

    return render(request, 'faculty_dashboard.html', {
        'faculty': faculty,
        'students_count': students_count,
        'notices_count': notices_count,
        'timetable_count': timetable_count
    })

def add_marks(request):
    if 'faculty_id' not in request.session:
        return redirect('faculty_login')

    if request.method == "POST":
        form = MarksForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('faculty_dashboard')
    else:
        form = MarksForm()

    return render(request, 'add_marks.html', {'form': form})

def add_attendance(request):
    if 'faculty_id' not in request.session:
        return redirect('faculty_login')

    if request.method == "POST":
        form = AttendanceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('faculty_dashboard')
    else:
        form = AttendanceForm()

    return render(request, 'add_attendance.html', {'form': form})

def add_timetable(request):
    if 'faculty_id' not in request.session:
        return redirect('faculty_login')

    if request.method == "POST":
        form = TimetableForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('faculty_dashboard')
    else:
        form = TimetableForm()

    return render(request, 'add_timetable.html', {'form': form})

def add_notice(request):
    if 'faculty_id' not in request.session:
        return redirect('faculty_login')

    if request.method == "POST":
        form = NoticeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('faculty_dashboard')
    else:
        form = NoticeForm()

    return render(request, 'add_notice.html', {'form': form})

def register(request):
    message = ""
    if request.method == "POST":
        form = StudentRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            message = "Registration Successful"
            form = StudentRegistrationForm()
        else:
            message = "Error in Registration. Please check inputs."
    else:
        form = StudentRegistrationForm()

    return render(request, 'register.html', {'form': form, 'message': message})

def search_student(request):
    student = None
    searched = False
    if request.method == "POST":
        roll = request.POST.get('roll_number')
        searched = True
        try:
            student = Student.objects.get(roll_number=roll)
        except Student.DoesNotExist:
            student = None

    return render(request, 'search_student.html', {
        'student': student, 
        'searched': searched
    })

# --- DATA MANAGEMENT MODULE VIEWS ---

def data_management_dashboard(request):
    """
    Renders the central Data Management dashboard panel for administrative functions.
    """
    if 'faculty_id' not in request.session:
        return redirect('faculty_login')
    
    try:
        faculty = Faculty.objects.get(faculty_id=request.session.get('faculty_id'))
    except Faculty.DoesNotExist:
        request.session.flush()
        return redirect('faculty_login')

    context = {
        'faculty': faculty,
        'student_count': Student.objects.count(),
        'faculty_count': Faculty.objects.count(),
        'attendance_count': Attendance.objects.count(),
        'marks_count': Marks.objects.count(),
        'timetable_count': Timetable.objects.count(),
        'notice_count': Notice.objects.count()
    }
    return render(request, 'data_management.html', context)

def import_students(request):
    """
    Handles student bulk registration spreadsheets (CSV/Excel) and reports status.
    """
    if 'faculty_id' not in request.session:
        return redirect('faculty_login')

    error_message = ""
    if request.method == "POST":
        form = BulkUploadForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = request.FILES['file']
            try:
                rows = parse_import_file(uploaded_file)
                results = import_students_from_list(rows)
                return render(request, 'import_results.html', {
                    'title': 'Student Import Results',
                    'results': results
                })
            except ValidationError as ve:
                error_message = ve.message
            except Exception as e:
                error_message = f"An unexpected error occurred: {str(e)}"
    else:
        form = BulkUploadForm()

    return render(request, 'import_form.html', {
        'title': 'Bulk Student Import',
        'description': 'Upload a CSV or Excel sheet containing Student columns: Name, Roll Number, Email, Branch, Year, Phone. GitHub Profile is optional.',
        'form': form,
        'error_message': error_message
    })

def import_faculty(request):
    """
    Handles faculty bulk registration spreadsheets (CSV/Excel) and reports status.
    """
    if 'faculty_id' not in request.session:
        return redirect('faculty_login')

    error_message = ""
    if request.method == "POST":
        form = BulkUploadForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = request.FILES['file']
            try:
                rows = parse_import_file(uploaded_file)
                results = import_faculty_from_list(rows)
                return render(request, 'import_results.html', {
                    'title': 'Faculty Import Results',
                    'results': results
                })
            except ValidationError as ve:
                error_message = ve.message
            except Exception as e:
                error_message = f"An unexpected error occurred: {str(e)}"
    else:
        form = BulkUploadForm()

    return render(request, 'import_form.html', {
        'title': 'Bulk Faculty Import',
        'description': 'Upload a CSV or Excel sheet containing Faculty columns: Name, Faculty ID, Department, Email, Password.',
        'form': form,
        'error_message': error_message
    })