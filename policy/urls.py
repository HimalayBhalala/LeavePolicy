from django.urls import path
from . import views

urlpatterns = [
    path('leave-type/',views.LaveTypeView.as_view(),name='leave-type'),
    path('get-leaves/',views.GetAllLeaveTypeView.as_view(),name='get-leaves')
]
