from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('status', views.get_status),
    path('start/<int:scenarioId>/', views.start)
]