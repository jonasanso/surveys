from django.test import TestCase

from surveys.models import Survey, SurveyResponse
from surveys.exceptions import NoMoreAvailablePlacesError


class SurveyResponseModelTests(TestCase):

    def test_reduce_available_places_after_creating_survey_response(self):
        """
        Creating a survey response must reduce by one the number of availabel places.
        """
        survey = Survey(name="first", available_places=10, user_id=1)
        survey.save()
        response = SurveyResponse(survey=survey, user_id=2)
        response.save()
        survey = Survey.objects.get(pk=survey.pk)
        self.assertIs(survey.available_places, 9)

    def test_raise_no_more_available_places_error_when_places_is_zero(self):
        """
        Creating a survey response must raise no more available error when places is zero.
        """
        with self.assertRaises(NoMoreAvailablePlacesError):
            survey = Survey(name="no more", available_places=0, user_id=1)
            survey.save()
            response = SurveyResponse(survey=survey, user_id=2)
            response.save()