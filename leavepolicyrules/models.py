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
    user = models.ForeignKey(User,on_delete=models.SET_NULL,null=True,blank=True)
    name = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name='leavetype'
        verbose_name_plural='leavetypes'
        db_table='leavetype'

    def __str__(self):
        return f"{self.name}"

class LeaveReason(models.Model):
    user = models.ForeignKey(User,on_delete=models.SET_NULL,null=True,blank=True)
    leave_type = models.ForeignKey(LeaveType,on_delete=models.CASCADE)
    reason = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'leavereason'
        verbose_name_plural = 'leavereasons'
        db_table = 'leavereason'

    def __str__(self):
        return f"{self.leave_type} - {self.reason}"

class LeaveRule(models.Model):
    user = models.ForeignKey(User,on_delete=models.SET_NULL,null=True)
    days = models.IntegerField()
    role = models.CharField(choices=ROLE_CHOOSES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'leaverule'
        verbose_name_plural = 'leaverules'
        db_table = 'leaverule'

    def __str__(self):
        return f"{self.role} - {self.days}"
