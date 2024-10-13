from django.urls import path
from . import views

urlpatterns = [
    path('emp/', views.create_employee, name='create_employee'),
    path('import-excel/', views.import_excel, name='import_excel'),
]