from django.contrib import admin
from .models import Medication
from .models import HealthRecord


admin.site.register(Medication)

@admin.register(HealthRecord)
class HealthRecordAdmin(admin.ModelAdmin):
    list_display = ('name', 'dob', 'condition')
    search_fields = ('name', 'condition')