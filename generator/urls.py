from django.urls import path
from . import views

urlpatterns = [
    path('download/<int:set_id>/', views.download, name='download'),
    path('', views.DataSchemaList.as_view(), name='schema-list'),
    path('set_list/<int:schema_id>/', views.DataSetList.as_view(), name='set-list'),
    path('create_schema/', views.create_data_schema, name='schema-create'),
    path('delete_schema/<int:schema_id>', views.delete_schema, name='schema-delete')
]
