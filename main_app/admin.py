from django.contrib import admin
from .models import Scenario, Action, Record
# Register your models here.
admin.site.register(Scenario)
admin.site.register(Action)
admin.site.register(Record)