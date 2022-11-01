# Map urls to view functions
from django.urls import path, re_path
from . import views

# URLConf
urlpatterns = [
    path('', views.IndexView.as_view()),
    path('search/', views.SearchView.as_view(), name='search'),
]
