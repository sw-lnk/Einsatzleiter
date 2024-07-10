from django.urls import path

from . import views

urlpatterns = [
    path('', views.dashboard, name="mission_dashboard"),
    path('all', views.all_missions, name="mission_all"),    
    path('add', views.add, name="mission_new"),
    path('overview/<int:main_id>/', views.mission_overview, name="mission_entry"),
    path('detail/<int:main_id>/', view=views.update, name='mission_update'),
    path('archiv/ask/<int:main_id>/', view=views.archiv_ask, name='mission_archiv_ask'),
    path('archiv/do/<int:main_id>/', view=views.archiv, name='mission_archiv_do'),
]