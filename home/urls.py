from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login, name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('profile/', views.profile, name='profile'),
    path('edit-profile/', views.edit_profile, name='edit_profile'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout, name='logout'),
    
    # Faculty Portal
    path('faculty-login/', views.faculty_login, name='faculty_login'),
    path('faculty-dashboard/', views.faculty_dashboard, name='faculty_dashboard'),
    path('add-attendance/', views.add_attendance, name='add_attendance'),
    path('add-marks/', views.add_marks, name='add_marks'),
    path('add-timetable/', views.add_timetable, name='add_timetable'),
    path('add-notice/', views.add_notice, name='add_notice'),
    
    # Data Management Portal
    path('data-management/', views.data_management_dashboard, name='data_management'),
    path('data-management/import-students/', views.import_students, name='import_students'),
    path('data-management/import-faculty/', views.import_faculty, name='import_faculty'),
    
    # Administration / Search
    path('search-student/', views.search_student, name='search_student'),
]