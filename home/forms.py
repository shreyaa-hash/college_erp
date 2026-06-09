from django import forms
from .models import Student, Faculty, Attendance, Marks, Timetable, Notice

class BootstrapModelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            existing_class = field.widget.attrs.get('class', '')
            if isinstance(field.widget, (forms.CheckboxInput, forms.RadioSelect)):
                field.widget.attrs['class'] = f"{existing_class} form-check-input".strip()
            elif isinstance(field.widget, forms.FileInput):
                field.widget.attrs['class'] = f"{existing_class} form-control".strip()
            else:
                field.widget.attrs['class'] = f"{existing_class} form-control form-control-custom".strip()

class StudentRegistrationForm(BootstrapModelForm):
    class Meta:
        model = Student
        fields = ['name', 'roll_number', 'branch', 'year', 'email', 'phone']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Enter Full Name'}),
            'roll_number': forms.TextInput(attrs={'placeholder': 'Enter Roll Number'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Enter Email Address'}),
            'branch': forms.TextInput(attrs={'placeholder': 'e.g., Computer Science'}),
            'year': forms.TextInput(attrs={'placeholder': 'e.g., 3rd Year'}),
            'phone': forms.TextInput(attrs={'placeholder': 'Enter 10-digit Phone'}),
        }

class StudentProfileForm(BootstrapModelForm):
    class Meta:
        model = Student
        fields = [
            'email', 'phone', 'branch', 'year', 'profile_pic', 
            'github_profile', 'study_hours_per_day', 'coding_hours_per_week', 
            'communication_score', 'stress_rating', 'dream_company', 
            'target_package', 'target_cgpa', 'assignments_completed', 'total_assignments'
        ]
        widgets = {
            'github_profile': forms.URLInput(attrs={'placeholder': 'https://github.com/username'}),
            'dream_company': forms.TextInput(attrs={'placeholder': 'e.g. Google, Microsoft'}),
        }

class AttendanceForm(BootstrapModelForm):
    class Meta:
        model = Attendance
        fields = ['student', 'subject', 'date', 'status']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }

class MarksForm(BootstrapModelForm):
    class Meta:
        model = Marks
        fields = ['student', 'subject', 'marks', 'total_marks']
        widgets = {
            'subject': forms.TextInput(attrs={'placeholder': 'e.g., Data Structures'}),
            'marks': forms.NumberInput(attrs={'placeholder': 'Marks Obtained'}),
            'total_marks': forms.NumberInput(attrs={'placeholder': 'Total Marks'}),
        }

class TimetableForm(BootstrapModelForm):
    class Meta:
        model = Timetable
        fields = ['day', 'subject', 'time', 'faculty']
        widgets = {
            'day': forms.TextInput(attrs={'placeholder': 'e.g., Monday'}),
            'subject': forms.TextInput(attrs={'placeholder': 'e.g., Computer Networks'}),
            'time': forms.TextInput(attrs={'placeholder': 'e.g., 10:00 AM - 11:00 AM'}),
            'faculty': forms.TextInput(attrs={'placeholder': 'Faculty Name'}),
        }

class NoticeForm(BootstrapModelForm):
    class Meta:
        model = Notice
        fields = ['title', 'message', 'subject', 'faculty', 'time']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Notice Title'}),
            'message': forms.Textarea(attrs={'placeholder': 'Write announcement here...', 'rows': 4}),
            'subject': forms.TextInput(attrs={'placeholder': 'Associated Subject (Optional)'}),
            'faculty': forms.TextInput(attrs={'placeholder': 'Publishing Faculty (Optional)'}),
            'time': forms.TextInput(attrs={'placeholder': 'Applicable Time Slot (Optional)'}),
        }

class BulkUploadForm(forms.Form):
    file = forms.FileField(
        label="Select Spreadsheet File",
        help_text="Upload a CSV (.csv) or Excel (.xlsx) file.",
        widget=forms.ClearableFileInput(attrs={'class': 'form-control form-control-custom'})
    )
