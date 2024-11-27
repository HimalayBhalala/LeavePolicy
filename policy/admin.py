from django.contrib import admin
from .models import *

# Register your models here.
@admin.register(LeaveRequest)
class LeaveRequestAdmin(admin.ModelAdmin):
    list_display = ("id","user","leave_type","custom_leave","leave_rule","leave_reason","hr_status","pm_status","tl_status","approved_by_hr","approved_by_pm","approved_by_tl","total_days","start_date","end_date")