from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', login_view, name='login'),
    path('signup/', signup_view, name='signup'),
    path('logout/', logout_view, name='logout'),
    path('landing-page',landingPage, name='landingPage'),
    path('medicationSchedule/',medicationSchedule, name='medication-schedule'),
    path('health-records/', add_record_view, name='health-records'),
    path('view-records/', view_records_view, name='view-records'),
    path('export-records/', export_records_view, name='export-records'),
    path('view-medication-schedule/', view_medication_schedule, name='view-medication-schedule'),
    path('add-medication/', add_medication, name='add-medication'),
    path('export-medication-schedule/', export_medication_schedule, name='export-medication-schedule'),
    path('update-record/<int:pk>/', update_record, name='update_record'),
    path('delete-record/<int:pk>/', delete_record, name='delete_record'),
    path('view-medication-schedule/', view_medication_schedule, name='view-medication-schedule'),
    path('view-patient-medications/<int:patient_id>/', view_patient_medications, name='view-patient-medications'),
    path('update-medication/<int:medication_id>/', update_medication, name='update-medication'),
    path('delete-medication/<int:medication_id>/', delete_medication, name='delete-medication'),
]

