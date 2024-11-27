from django.db import models
from leavepolicyrules.models import *

LEAVE_STATUS = (
    (0,'Rejected'),
    (1,'Approved'),
    (2,'Pending'),
)

class LeaveRequest(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    leave_type = models.ForeignKey(LeaveType,on_delete=models.CASCADE)
    custom_leave = models.CharField(max_length=200,null=True,blank=True)
    leave_rule = models.ForeignKey(LeaveRule,on_delete=models.CASCADE)
    leave_reason = models.ForeignKey(LeaveReason,on_delete=models.CASCADE)
    leave_description = models.TextField(max_length=500)
    admin_status = models.IntegerField(choices=LEAVE_STATUS,default=2)
    hr_status = models.IntegerField(choices=LEAVE_STATUS,default=2)
    pm_status = models.IntegerField(choices=LEAVE_STATUS,default=2)
    tl_status = models.IntegerField(choices=LEAVE_STATUS,default=2)
    approved_by_admin = models.ForeignKey(User,on_delete=models.SET_NULL,related_name='approved_by_admin',null=True,blank=True)
    approved_by_hr = models.ForeignKey(User,on_delete=models.SET_NULL,related_name='approved_by_hr',null=True,blank=True)
    approved_by_pm = models.ForeignKey(User,on_delete=models.SET_NULL,related_name='approved_by_pm',null=True,blank=True)
    approved_by_tl = models.ForeignKey(User,on_delete=models.SET_NULL,related_name='approved_by_tl',null=True,blank=True)
    total_days = models.IntegerField(null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    start_date = models.DateField()
    end_date = models.DateField()

    class Meta:
        verbose_name = 'leaverequest'
        verbose_name_plural = 'leaverequests'
        db_table = 'leaverequest'
