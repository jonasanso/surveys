from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from surveys.models import Survey, SurveyResponse

class SurveyTests(APITestCase):
    def test_create_survey(self):
        """
        Ensure we can create a new survey object.
        """
        url = 'http://testserver/surveys/'
        data = {'name': 'test1', 'available_places': 1, 'user_id': 1}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Survey.objects.count(), 1)
        self.assertEqual(Survey.objects.get().id, 1)
        self.assertEqual(Survey.objects.get().name, 'test1')
        self.assertEqual(Survey.objects.get().available_places, 1)
        self.assertEqual(Survey.objects.get().user_id, 1)

    def test_list_surveys(self):
        """
        Ensure we can list created surveys.
        """
        Survey(name='test2', available_places=1, user_id=1).save()
        url = 'http://testserver/surveys/'
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, [{'id': 1, 'name': 'test2', 'available_places': 1, 'user_id': 1}])


class SurveyResponseTests(APITestCase):
    def test_create_survey_response(self):
        """
        Ensure we can create a new survey response object.
        """
        Survey(name='test3', available_places=1, user_id=1).save()
        url = 'http://testserver/survey-responses/'
        data = {'survey_id': 1, 'user_id': 2}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(SurveyResponse.objects.count(), 1)
        
        survey_response = SurveyResponse.objects.get()
        self.assertEqual(survey_response.id, 1)
        self.assertEqual(survey_response.survey_id, 1)
        self.assertEqual(survey_response.user_id, 2)
        self.assertIsNotNone(survey_response.created_at)

