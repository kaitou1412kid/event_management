from django.urls import include, path
from . import views
urlpatterns = [
    path('create-event/', views.EventAPIView.as_view(), name='create-event'),
    path('events/', views.EventAPIView.as_view(), name='view-event'),
    path('events/<int:event_id>/', views.EventAPIView.as_view(), name='view-event'),
    path('events/<int:event_id>/rsvp/', views.RSVPView.as_view(), name='RSVP'),
    path('events/<int:event_id>/feedback/', views.FeedbackView.as_view(),name='Feedback'),
    path('events/<int:event_id>/attendance/', views.AttendanceView.as_view(),name='Attendance'),
]