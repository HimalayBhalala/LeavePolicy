from django.db import models
from leavepolicyrules.models import *
from datetime import date

class LeaveRequest(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    leave_type = models.ForeignKey(LeaveType,on_delete=models.CASCADE)
    custom_leave = models.CharField(max_length=200,null=True,blank=True)
    leave_rule = models.ForeignKey(LeaveRule,on_delete=models.CASCADE)
    leave_reason = models.ForeignKey(LeaveReason,on_delete=models.CASCADE)
    leave_description = models.TextField(max_length=500)
    status = models.CharField(max_length=10,choices=LEAVE_STATUS,default='pending')
    approved_by = models.ForeignKey(User,on_delete=models.SET_NULL,related_name='approved_by',null=True)
    requested_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # start_date = models.DateField(default=date)
    # end_date = models.DateField()

    class Meta:
        verbose_name = 'leaverequest'
        verbose_name_plural = 'leaverequests'
        db_table = 'leaverequest'
