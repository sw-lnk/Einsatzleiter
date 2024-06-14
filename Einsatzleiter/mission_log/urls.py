from django.urls import path

from . import views

urlpatterns = [
    path('', views.all_missions, name="mission"),
    path('add', views.add, name="mission_new"),
    path('update/<int:main_id>/', view=views.update, name='mission_update'),
    path('archiv/ask/<int:main_id>/', view=views.archiv_ask, name='mission_archiv_ask'),
    path('archiv/do/<int:main_id>/', view=views.archiv, name='mission_archiv_do'),
]