from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.template import loader
from django.views.decorators.http import require_http_methods
from .scrapper import scrapper
from .models import *
import json

# Create your views here.
def index(request):
    template = loader.get_template('index.html')
    return HttpResponse(template.render(None, request ))
# @require_http_methods(["POST"])
def get_status(request):
    scrapper.commands.append("test")
    # parsed = json.loads(request.body.decode('utf-8'))
    # print(parsed)
    response_data = {}
    allScenarios = Scenario.objects.all()
    for scenario in allScenarios:
        actions = Action.objects.filter(scenario=scenario.pk)
        response_data[scenario.name] = list(map(lambda a: a.__str__(), actions))
    return JsonResponse(response_data)

def start(request, scenarioId):
    scrapper.scraper.start(scenarioId)
    return HttpResponse("ok")