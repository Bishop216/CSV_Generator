from django.urls import path
from . import views

urlpatterns = [
    path('download/<int:set_id>/', views.download, name='download'),
    path('schema_list/', views.DataSchemaList.as_view(), name='schema-list'),
    path('set_list/<int:schema_id>/', views.DataSetList.as_view(), name='set-list')
]
