from django.db import models
from .scrapper.action_types import ActionTypes
# Create your models here.
class Scenario(models.Model):
    name = models.CharField(max_length=200)
    created_date = models.DateTimeField('date published', auto_now=True)
    def __str__(self):
        return self.name


class Action(models.Model):
    scenario = models.ForeignKey(Scenario, on_delete=models.CASCADE)
    actionType = models.IntegerField()
    params = models.JSONField(null=True, blank=True)
    parentId = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    def __str__(self):
        return ActionTypes(self.actionType).name + ' ' + self.scenario.__str__()

class Record(models.Model):
    created_date = models.DateTimeField('date created', auto_now=True)
    scenario = models.ForeignKey(Scenario, on_delete=models.CASCADE)
    data = models.JSONField(null=True, blank=True)
    screen = models.ImageField(null=True)
