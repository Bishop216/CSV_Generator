from django import forms
from .models import DataSchema, Column, DataSet


class DataSchemeForm(forms.ModelForm):
    class Meta:
        model = DataSchema
        fields = [
            'name'
        ]


class ColumnForm(forms.ModelForm):
    class Meta:
        model = Column
        fields = [
            'name',
            'order',
            'data_type',
            'value_range_from',
            'value_range_to'
        ]


class DataSetForm(forms.ModelForm):
    class Meta:
        model = DataSet
        fields = [
            'rows'
        ]
