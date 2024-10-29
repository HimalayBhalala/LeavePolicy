from django.contrib import admin
from .models import *

# Register your models here.
@admin.register(LeaveRequest)
class LeaveRequestAdmin(admin.ModelAdmin):
    list_display = ("id","user","leave_type","custom_leave","leave_rule","leave_reason","status","approved_by","requested_date")