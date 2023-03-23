"""matrix_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path, include
from matrix_calculator import views
from django.contrib import admin
from django.urls import path

urlpatterns = [
    path('matrix_calculator/', views.matrix_calculator, name='matrix_calculator'),
    path('practice_questions/', views.practice_questions, name='practice_questions'),
    path('menu/', views.menu, name='menu'),
    path('create_exercises/', views.create_exercises, name='create_exercises'),
    path('create_new_exercise/', views.create_new_exercise, name='create_new_exercise'),
    path('add_questions/', views.add_questions, name='add_questions'),
]
