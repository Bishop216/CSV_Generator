from django import forms
from .models import DataSchema, Column, DataSet, DATA_TYPES
from django.forms import formset_factory


class DataSchemaForm(forms.ModelForm):
    class Meta:
        model = DataSchema
        fields = [
            'name'
        ]


class ColumnForm(forms.ModelForm):
    value_range_from = forms.IntegerField(label='from', required=False, initial=1)
    value_range_to = forms.IntegerField(label='to', required=False, initial=100)
    data_type = forms.ChoiceField(choices=DATA_TYPES)

    class Meta:
        model = Column
        fields = [
            'name',
            'data_type',
            'value_range_from',
            'value_range_to',
            'order'
        ]


ColumnFormSet = formset_factory(
    ColumnForm,
    extra=0,
    min_num=1
)


class DataSetForm(forms.ModelForm):
    class Meta:
        model = DataSet
        fields = [
            'rows'
        ]
