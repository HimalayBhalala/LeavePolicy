from django.urls import path
from . import views

urlpatterns = [
    path('leave-request/',views.LeaveRequestView.as_view(),name='leave-request'),
    path('get-all-request/',views.GetAllLeaveRequestView.as_view(),name='get-all-request'),
    path('get-request/<int:pk>/',views.ApprovedRequestView.as_view(),name='get-request')
]
