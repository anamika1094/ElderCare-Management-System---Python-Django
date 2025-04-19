from django.db import models
from django.contrib import admin


#Create your models here

from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class HealthRecord(models.Model):
    name = models.CharField(max_length=100)
    dob = models.DateField(verbose_name="Date of Birth")
    condition = models.TextField(verbose_name="Medical Condition")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.dob}"


class HealthRecordForm(forms.ModelForm):
    class Meta:
        model = HealthRecord
        fields = ['name', 'dob', 'condition']
        widgets = {
            'dob': forms.DateInput(attrs={'type': 'date'}),
            'condition': forms.Textarea(attrs={'rows': 4}),
        }

from django.db import models

class Medication(models.Model):
    FREQUENCY_CHOICES = [
        ('once', 'Once a day'),
        ('twice', 'Twice a day'),
        ('thrice', 'Thrice a day'),
    ]

    health_record = models.ForeignKey(HealthRecord, on_delete=models.CASCADE, related_name="medications", verbose_name="Health Record")
    name = models.CharField(max_length=100, verbose_name="Medication Name")
    dose = models.CharField(max_length=50, verbose_name="Dose", help_text="e.g., 500mg")
    frequency = models.CharField(max_length=10, choices=FREQUENCY_CHOICES, verbose_name="Frequency")
    time = models.TimeField(verbose_name="Time", help_text="Time to take the medication")

    def __str__(self):
        return f"{self.name} ({self.dose}) - {self.get_frequency_display()}"




class MedicationAdmin(admin.ModelAdmin):
    list_display = ('name', 'dose', 'frequency', 'time', 'added_on')
    list_filter = ('frequency', 'added_on')
    search_fields = ('name', 'dose')
    