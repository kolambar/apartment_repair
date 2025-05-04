from django.urls import path
from . import views
from .apps import RepairConfig

app_name = RepairConfig.name

urlpatterns = [
    path('flat_list/', views.flat_list, name='flat_list'),
    path('add_flat/', views.add_flat, name='add_flat'),
    path('flat_detail/<int:pk>/', views.flat_detail, name='flat_detail'),
    path('flat/<int:flat_id>/add_operation/', views.add_operation, name='add_operation'),
    path('', views.main_menu, name='main_menu'),
    path('report/workers/', views.report_workers, name='report_workers'),
    path('report/repairs/', views.report_repairs, name='report_repairs'),
    path('report/work_type/', views.report_by_work_type, name='report_by_work_type'),
]
