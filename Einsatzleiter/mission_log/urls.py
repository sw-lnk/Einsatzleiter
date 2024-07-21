from django.urls import path

from . import views

urlpatterns = [
    path('', views.dashboard, name="mission_dashboard"),
    
    path('mission_all', views.all_missions, name="mission_all"),    
    path('mision_add', views.add, name="mission_new"),
    path('mission_overview/<int:main_id>/', views.mission_overview, name="mission_overview"),
    path('mission_detail/<int:main_id>/', view=views.update, name='mission_detail'),
    path('mission_report/<int:main_id>/', view=views.download_report, name='mission_report'),
    path('mission_archiv/ask/<int:main_id>/', view=views.archiv_ask, name='mission_archiv_ask'),
    path('mission_archiv/do/<int:main_id>/', view=views.archiv, name='mission_archiv_do'),
    
    path('unit_all', views.all_units, name="unit_all"),
    path('unit_add', views.unit_add, name="unit_new"),    
    path('unit_detail/<int:pk>/', views.unit_update, name="unit_detail"),
]