from django.contrib import admin
from .models import *

# Register your models here.

@admin.register(LeaveType)
class LeaveTypeAdmin(admin.ModelAdmin):
    list_display = ['id','user','name','created_at','updated_at']

@admin.register(LeaveReason)
class LeaveReasonAdmin(admin.ModelAdmin):
    list_display = ["id","user","leave_type","created_at","updated_at"]

@admin.register(LeaveRule)
class LeaveRuleAdmin(admin.ModelAdmin):
    list_display = ("id","user","days","role",'created_at','updated_at')
