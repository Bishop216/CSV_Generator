from django.urls import path
from . import views

urlpatterns = [
    path('download/<int:set_id>/', views.download)
]
