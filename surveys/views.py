from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from surveys.exceptions import NoMoreAvailablePlacesError
from surveys.models import Survey, SurveyResponse
from surveys.serializers import SurveySerializer, SurveyResponseSerializer

@api_view(['GET', 'POST'])
def surveys(request):
    """
    List surveys with optinal user_id filter, or create a new survey.
    """
    if request.method == 'GET':
        user_id = request.query_params.get('user_id', None)
        if user_id is not None:
            surveys = Survey.objects.filter(user_id=user_id)
        else: 
            surveys = Survey.objects.all()
        serializer = SurveySerializer(surveys, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = SurveySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST'])
def responses_to_survey(request, survey_id):
    """
    Retrieve survey responses for survey identified by pk.
    """
    if request.method == 'GET':
        responses = SurveyResponse.objects.filter(survey__pk = survey_id)
        serializer = SurveyResponseSerializer(responses, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        request.data['survey_id'] = survey_id
        serializer = SurveyResponseSerializer(data=request.data)
        if serializer.is_valid():
            try:
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except NoMoreAvailablePlacesError: 
                return Response(status=status.HTTP_410_GONE)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def survey_responses(request):
    """
    List all surveys responses optionally filtered by user_id, or create a new survey response.
    """
    if request.method == 'GET':
        user_id = request.query_params.get('user_id', None)
        if user_id is not None:
            responses = SurveyResponse.objects.filter(user_id=user_id)
        else: 
            responses = SurveyResponse.objects.all()
        serializer = SurveyResponseSerializer(responses, many=True)
        return Response(serializer.data)

