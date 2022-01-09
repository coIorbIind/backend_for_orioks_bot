from django.urls import path

from .views import *

urlpatterns = [
    path('marks/', GetMarksView.as_view(), name='get_marks'),
    path('check/', CheckMarksView.as_view(), name='check_marks'),
    path('create/', CreateUserView.as_view(), name='register')
]
