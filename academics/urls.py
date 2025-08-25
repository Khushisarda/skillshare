# academics/urls.py
from django.urls import path
from . import views

app_name = 'academics'

urlpatterns = [
    # Main pages
    path('', views.dashboard_view, name='dashboard'),
    path('notes/', views.notes_view, name='notes'),
    path('pyqs/', views.pyqs_view, name='pyqs'),
    path('books/', views.books_view, name='books'),
    path('resource/<int:pk>/', views.resource_detail_view, name='resource_detail'),
    
    path('ajax/years/', views.get_years_by_department, name='get_years_by_department'),
    path('ajax/subjects/', views.get_subjects_by_department_year, name='get_subjects_by_department_year'),

]
