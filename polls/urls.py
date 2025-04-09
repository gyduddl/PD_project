from django.urls import path
from django.views.generic import TemplateView

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:question_id>/', views.detail, name='detail'),
    path('<int:question_id>/results/', views.results, name="results"),
    path('<int:question_id>/vote/', views.vote, name='vote'),
    path('<int:question_id>/reset/', views.reset, name='reset'),
    path('<int:question_id>/likes/', views.likes, name='likes'),
    path('new/', TemplateView.as_view(template_name="polls/new.html"), name='new'),
    path('create/', views.create, name='create'),
    path('delete/<int:question_id>/', views.delete, name='delete'),
    path('<int:question_id>/modify/', views.modify, name='modify'),
    path('update/<int:question_id>/', views.update, name='update'),
]