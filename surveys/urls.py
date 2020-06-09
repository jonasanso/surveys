from django.urls import path
from surveys import views

urlpatterns = [
    path('surveys/', views.surveys),
    path('surveys/<int:survey_id>/responses/', views.responses_to_survey),
    path('survey-responses/', views.survey_responses),
]