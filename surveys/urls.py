from django.urls import path
from surveys import views

urlpatterns = [
    path('surveys/', views.survey_list),
    path('surveys/<int:pk>/', views.survey_detail),
]