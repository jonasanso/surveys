from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from surveys.models import Survey
from surveys.serializers import SurveySerializer

@api_view(['GET', 'POST'])
def survey_list(request):
    """
    List all code surveys, or create a new snippet.
    """
    if request.method == 'GET':
        surveys = Survey.objects.all()
        serializer = SurveySerializer(surveys, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = SurveySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def survey_detail(request, pk):
    """
    Retrieve, update or delete a code survey.
    """
    try:
        snippet = Survey.objects.get(pk=pk)
    except Survey.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = SurveySerializer(snippet)
        return Response(serializer.data)