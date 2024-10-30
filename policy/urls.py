from django.urls import path
from . import views

urlpatterns = [
    # Add a Leave Request Api
    path('leave-request/',views.LeaveRequestView.as_view(),name='leave-request'),
    path('get-all-request/',views.GetAllLeaveRequestView.as_view(),name='get-all-request'),
    path('get-request/<int:pk>/',views.ApprovedRequestView.as_view(),name='get-request'),
    
    # Filter - Based api
    path('filter/',views.FilterDataView.as_view(),name='filter-data')
]



