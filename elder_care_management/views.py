from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from .models import *
from django.contrib import messages
import csv
from django.http import HttpResponse
from .models import Medication
from django.shortcuts import render, redirect, get_object_or_404
from .models import HealthRecord
from .models import HealthRecordForm
from django.contrib.auth.decorators import login_required



def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"Welcome back, {user.username}!")
                return redirect('landingPage')  # Redirect to health-records page
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def signup_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f"Account created for {user.username}!")
            return redirect('login')  # Redirect to landingPage page
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = CustomUserCreationForm()
    return render(request, 'signup.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect('login')  # Redirect to login page

@login_required
def add_record_view(request):
    if request.method == 'POST':
        form = HealthRecordForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Health record added successfully!")
            return redirect('landingPage')
        else:
            messages.error(request, "Please correct the errors in the form.")
    else:
        form = HealthRecordForm()
    return render(request, 'health-records.html', {'form': form})

@login_required
def view_records_view(request):
    records = HealthRecord.objects.all().order_by('-created_at')
    return render(request, 'view_records.html', {'records': records})

@login_required
# View to display all health records
def view_records(request):
    records = HealthRecord.objects.all()
    return render(request, 'view_records.html', {'records': records})

@login_required
def export_records_view(request):
    records = HealthRecord.objects.all()

    # Create CSV response
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="health-records.csv"'

    writer = csv.writer(response)
    writer.writerow(['Name', 'Date of Birth', 'Medical Condition', 'Created At'])

    for record in records:
        writer.writerow([record.name, record.dob, record.condition, record.created_at])

    return response

@login_required
def landingPage(request):
    return render(request,'landing-page.html')

@login_required
def healthRecords(request):
    return render(request,'health-records.html')

@login_required
def medicationSchedule(request):
    return render(request,'medication-schedule.html')

@login_required
def add_medication(request):
    if request.method == 'POST':
        health_record_id = request.POST.get('patient')
        medication_name = request.POST.get('medication-name')
        dose = request.POST.get('dose')
        frequency = request.POST.get('frequency')
        time = request.POST.get('time')

        # Get the HealthRecord instance
        health_record = HealthRecord.objects.get(id=health_record_id)

        # Save the medication with the associated health record
        Medication.objects.create(health_record=health_record, name=medication_name, dose=dose, frequency=frequency, time=time)

        return redirect('view-medication-schedule')

    # Pass health records to the template
    health_records = HealthRecord.objects.all()
    return render(request, 'add_medication.html', {'health_records': health_records})



@login_required
def view_medication_schedule(request):
    # Fetch all patients (HealthRecords)
    patients = HealthRecord.objects.all()
    return render(request, 'view_medication_schedule.html', {'patients': patients})


@login_required
def view_patient_medications(request, patient_id):
    # Get the selected patient
    patient = HealthRecord.objects.get(id=patient_id)

    # Fetch medications linked to the patient
    medications = Medication.objects.filter(health_record=patient)
    return render(request, 'patient_medications.html', {
        'patient': patient,
        'medications': medications,
    })

@login_required
def update_medication(request, medication_id):
    medication = Medication.objects.get(id=medication_id)

    if request.method == 'POST':
        medication.name = request.POST.get('medication-name')
        medication.dose = request.POST.get('dose')
        medication.frequency = request.POST.get('frequency')
        medication.time = request.POST.get('time')
        medication.save()
        return redirect('view-patient-medications', patient_id=medication.health_record.id)

    return render(request, 'update_medication.html', {'medication': medication})


@login_required
def delete_medication(request, medication_id):
    medication = Medication.objects.get(id=medication_id)
    patient_id = medication.health_record.id
    medication.delete()
    return redirect('view-patient-medications', patient_id=patient_id)

@login_required
def export_medication_schedule(request):
    # Example export logic (can be replaced with CSV export or similar)
    medications = Medication.objects.all()
    response = "Medication Schedule:\n"
    for med in medications:
        response += f"{med.name} - {med.dose}, {med.frequency}, at {med.time}\n"
    return HttpResponse(response, content_type='text/plain')

@login_required
def update_medication(request, medication_id):
    medication = get_object_or_404(Medication, id=medication_id)
    
    if request.method == 'POST':
        medication.name = request.POST.get('medication-name')
        medication.dose = request.POST.get('dose')
        medication.frequency = request.POST.get('frequency')
        medication.time = request.POST.get('time')
        medication.save()
        messages.success(request, "Medication updated successfully!")
        return redirect('view-patient-medications', patient_id=medication.health_record.id)

    return render(request, 'update_medication.html', {'medication': medication})

@login_required
def delete_medication(request, medication_id):
    medication = get_object_or_404(Medication, id=medication_id)
    patient_id = medication.health_record.id

    if request.method == 'POST':
        medication.delete()
        messages.success(request, "Medication deleted successfully!")
        return redirect('view-patient-medications', patient_id=patient_id)

    return render(request, 'delete_medication.html', {'medication': medication})

@login_required
# View to update a record
def update_record(request, pk):
    record = get_object_or_404(HealthRecord, pk=pk)
    if request.method == 'POST':
        form = HealthRecordForm(request.POST, instance=record)
        if form.is_valid():
            form.save()
            return redirect('view-records')
    else:
        form = HealthRecordForm(instance=record)
    return render(request, 'update_record.html', {'form': form, 'record': record})

@login_required
# View to delete a record
def delete_record(request, pk):
    record = get_object_or_404(HealthRecord, pk=pk)
    if request.method == 'POST':
        record.delete()
        return redirect('view-records')
    return render(request, 'delete_record.html', {'record': record})