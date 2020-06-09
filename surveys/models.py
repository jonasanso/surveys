from django.db import models
from django.db.models import CheckConstraint, Q, F
from django.utils import timezone

class Survey(models.Model):
    name = models.CharField(max_length=200)
    available_places = models.IntegerField()
    user_id = models.IntegerField()

    def __str__(self):
        return self.name

    class Meta:
        constraints = [
           CheckConstraint(check=Q(available_places__gte=0), name='available_places_is_a_whole_number'),
        ]
        indexes = [
            models.Index(fields=['user_id'], name='user_surveys_idx')
        ]


class SurveyResponse(models.Model):
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE)
    user_id = models.IntegerField()
    created_at = models.DateTimeField('date created', auto_now_add=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  
        self.survey.available_places =  F('available_places') - 1
        self.survey.save()

    def __str__(self):
        return "Survey %s by user %s at %s " % (self.survey.name, self.user_id, self.created_at)

    class Meta:
        indexes = [
            models.Index(fields=['survey_id', 'user_id'], name='user_survey_responses_idx')
        ]