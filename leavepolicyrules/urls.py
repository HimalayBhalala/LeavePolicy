from django.urls import path
from . import views

urlpatterns = [

    # Leave-Type Functionality
    path('leave-type/',views.LeaveTypeView.as_view(),name='leave-type'),
    path('get-leaves/',views.GetAllLeaveTypeView.as_view(),name='get-leaves'),
    path('leave-type/<int:pk>/',views.LeaveTypeView.as_view(),name='get-edit-delete-leave-type'),

    # Leave-Reason Functionality
    path('leave-reason/',views.LeaveReasonView.as_view(),name='leave-reason'),
    path('get-reasons/',views.GetAllLeaveReasonView.as_view(),name='get-reasons'),
    path('leave-reason/<int:pk>/',views.LeaveReasonView.as_view(),name='get-edit-delete-reason'),

    # Leave-Rule Functionality
    path('leave-rule/',views.LeaveRuleView.as_view(),name='leave-rule'),
    path('get-rules/',views.GetAllLeaveRuleView.as_view(),name='get-reule'),
    path('leave-rule/<int:pk>/',views.LeaveRuleView.as_view(),name='get-edit-delete-rule')
]
