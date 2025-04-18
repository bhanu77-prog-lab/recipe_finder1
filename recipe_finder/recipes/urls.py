from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('recipes.urls')),
]

# filepath: c:\Users\ADMIN\recipe_finder\recipe_finder\recipes\urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.recipe_finder_view, name='recipe_finder'),
]