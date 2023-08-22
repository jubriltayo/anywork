from django.contrib import admin
from django.urls import path
from pages.views import home_view
from professionals.views import (professional_detail_view,
                                 professional_list_view,
                                 professional_delete_view,
                                 professional_service_view,
                                 professional_update_view,
                                 professional_success_view
)
app_name = 'professional'

urlpatterns = [
    path('', professional_list_view, name='professional-list'),
    path('success/', professional_success_view, name='professional-success'),
    path('<int:id>/', professional_detail_view, name='professional-detail'),
    path('<int:id>/delete/', professional_delete_view, name='professional-delete'),
    path('<int:id>/update/', professional_update_view, name='professional-update'),
    path('<str:service>/', professional_service_view, name='professional-service'),
]
