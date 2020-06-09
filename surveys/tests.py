import datetime

from django.test import TestCase
from django.utils import timezone

from surveys.models import Survey, SurveyResponse


class SurveyResponseModelTests(TestCase):

    def test_reduce_available_plaves_after_creating_survey_response(self):
        """
        Creating a survey response must reduce by one the number of availabel places.
        """
        survey = Survey(name="first", available_places=10, user_id=1)
        survey.save()
        response = SurveyResponse(survey=survey, user_id=2)
        response.save()
        survey = Survey.objects.get(pk=survey.pk)
        self.assertIs(survey.available_places, 9)