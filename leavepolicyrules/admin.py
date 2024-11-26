from django.contrib import admin
from .models import *

# Register your models here.

@admin.register(LeaveType)
class LeaveTypeAdmin(admin.ModelAdmin):
    list_display = ['id','user','name','status','created_at','updated_at']

@admin.register(LeaveReason)
class LeaveReasonAdmin(admin.ModelAdmin):
    list_display = ["id","user","leave_type",'status',"created_at","updated_at"]

@admin.register(LeaveRule)
class LeaveRuleAdmin(admin.ModelAdmin):
    list_display = ("id","user","days","role",'status','created_at','updated_at')
