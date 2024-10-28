from django.db import models
from authentication.models import User
from authentication.models import ROLE_CHOOSES

# Create your models here.

LEAVE_STATUS = (
    ('approved','Approved'),
    ('pending','Pending'),
    ('rejected','Rejected')
)

class LeaveType(models.Model):
    user = models.ForeignKey(User,on_delete=models.SET_NULL,null=True)
    name = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

def __str__(self):
    return self.name

class LeaveReason(models.Model):
    user = models.ForeignKey(User,on_delete=models.SET_NULL,null=True)
    leave_type = models.ForeignKey(LeaveType,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class LeaveRule(models.Model):
    user = models.ForeignKey(User,on_delete=models.SET_NULL,null=True)
    leave_type = models.ForeignKey(LeaveType,on_delete=models.CASCADE)
    days = models.DateField(null=True,blank=True)
    role = models.CharField(choices=ROLE_CHOOSES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class LeaveRequest(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    leave_type = models.ForeignKey(LeaveType,on_delete=models.CASCADE)
    custom_leave = models.CharField(max_length=200,null=True,blank=True)
    leave_rule = models.ForeignKey(LeaveRule,on_delete=models.SET_NULL,null=True)
    leave_reason = models.ForeignKey(LeaveReason,on_delete=models.SET_NULL,null=True)
    leave_description = models.TextField(max_length=500)
    status = models.CharField(max_length=10,choices=LEAVE_STATUS,default='pending')
    approved_by = models.ForeignKey(User,on_delete=models.SET_NULL,related_name='approved_by',null=True)
    start_date = models.DateField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    
