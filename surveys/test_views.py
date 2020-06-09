import datetime

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from surveys.models import Survey, SurveyResponse

from django.utils import timezone

class SurveyTests(APITestCase):
    def test_list_all_surveys(self):
        """
        Ensure we can list created surveys.
        """
        Survey(name='test_list_all_surveys', available_places=1, user_id=1).save()

        url = 'http://testserver/surveys/'
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, [{'id': 1, 'name': 'test_list_all_surveys', 'available_places': 1, 'user_id': 1}])

    def test_create_survey(self):
        """
        Ensure we can create a new survey object.
        """
        url = 'http://testserver/surveys/'
        data = {'name': 'test_create_survey', 'available_places': 1, 'user_id': 1}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Survey.objects.count(), 1)
        self.assertEqual(Survey.objects.get().id, 1)
        self.assertEqual(Survey.objects.get().name, 'test_create_survey')
        self.assertEqual(Survey.objects.get().available_places, 1)
        self.assertEqual(Survey.objects.get().user_id, 1)

    def test_create_survey_response(self):
        """
        Ensure we can create a new survey response object.
        """
        Survey(name='test3', available_places=1, user_id=1).save()

        url = 'http://testserver/surveys/1/responses/'
        data = {'user_id': 2}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(SurveyResponse.objects.count(), 1)
        
        survey_response = SurveyResponse.objects.get()
        self.assertEqual(survey_response.id, 1)
        self.assertEqual(survey_response.survey_id, 1)
        self.assertEqual(survey_response.user_id, 2)
        self.assertIsNotNone(survey_response.created_at)

    def test_list_surveys_belonging_to_a_user(self):
        """
        Ensure we can list created surveys.
        """
        Survey(name='test_list_surveys_belonging_to_a_user', available_places=1, user_id=1).save()

        url = 'http://testserver/surveys/?user_id=1'
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, [{'id': 1, 'name': 'test_list_surveys_belonging_to_a_user', 'available_places': 1, 'user_id': 1}])

        url = 'http://testserver/surveys/?user_id=2'
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, [])

    def test_responses_to_survey(self):
        """
        Ensure we can list created responses for a survey.
        """
        now = timezone.now()
        Survey(name='test responses_to_survey', available_places=1, user_id=1).save()
        survey = Survey.objects.get()
        self.assertEqual(survey.id, 1)
        SurveyResponse(survey=survey, user_id=2, created_at=now).save()

        url = 'http://testserver/surveys/1/responses/'
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['id'], 1)
        self.assertEqual(response.data[0]['survey_id'], 1)
        self.assertEqual(response.data[0]['user_id'], 2)
        self.assertIsNotNone(response.data[0]['created_at'])

    def test_survey_responses_belonging_to_user(self):
        """
        Ensure we can list all created responses belonging to a user.
        """
        now = timezone.now()
        Survey(name='test responses_to_survey', available_places=1, user_id=1).save()
        survey = Survey.objects.get()
        self.assertEqual(survey.id, 1)
        SurveyResponse(survey=survey, user_id=2, created_at=now).save()

        url = 'http://testserver/survey-responses/?user_id=2'
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['id'], 1)
        self.assertEqual(response.data[0]['survey_id'], 1)
        self.assertEqual(response.data[0]['user_id'], 2)
        self.assertIsNotNone(response.data[0]['created_at'])

        url = 'http://testserver/survey-responses/?user_id=3'
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, [])