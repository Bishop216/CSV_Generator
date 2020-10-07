import os
from django.http import FileResponse, HttpResponse, HttpResponseRedirect
from django.conf import settings
from django.shortcuts import redirect, render
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import DataSet, DataSchema, Column
from .forms import DataSetForm, DataSchemaForm, ColumnFormSet
from .tasks import generate_csv


def create_data_schema(request):
    """
    View responsible for data schemas creation.
    :param request:
    :return:
    """
    template_name = 'data_schema_creation.html'

    if request.method == 'GET':
        schema_form = DataSchemaForm(request.GET or None)
        formset = ColumnFormSet()

    elif request.method == 'POST':
        schema_form = DataSchemaForm(request.POST)
        formset = ColumnFormSet(request.POST)

        if schema_form.is_valid() and formset.is_valid():
            schema_data = schema_form.cleaned_data
            columns_data = formset.cleaned_data

            new_schema = DataSchema(name=schema_data['name'],
                                    user=request.user)
            new_schema.save()

            for column in columns_data:
                new_column = Column(schema=new_schema,
                                    name=column['name'],
                                    data_type=column['data_type'],
                                    order=column['order'],
                                    value_range_from=column.get('value_range_from'),
                                    value_range_to=column.get('value_range_to'))

                new_column.save()

            return redirect('schema-list')

    return render(request, template_name, {
        'schema_form': schema_form,
        'formset': formset
    })


class DataSchemaList(LoginRequiredMixin, ListView):
    """
    View that lists user data schemas.
    """
    model = DataSchema
    template_name = 'data_schema_list.html'

    def get_queryset(self):
        self.queryset = DataSchema.objects.filter(user=self.request.user)
        return super(DataSchemaList, self).get_queryset()


class DataSetList(LoginRequiredMixin, ListView):
    """
    View responsible for listing and creating data sets related to specific data schema.
    """
    model = DataSet
    template_name = 'data_set_list.html'
    form_class = DataSetForm

    def get_queryset(self):
        schema_id = self.kwargs['schema_id']
        self.queryset = DataSet.objects.filter(schema_id=schema_id)
        return super(DataSetList, self).get_queryset()

    def get_context_data(self, **kwargs):
        context = super(DataSetList, self).get_context_data()
        context['form'] = self.form_class()
        return context

    def post(self, request, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            rows = form.cleaned_data['rows']
            schema_id = self.kwargs['schema_id']

            data_schema = DataSchema.objects.get(pk=schema_id)

            new_data_set = DataSet(rows=rows, schema=data_schema)
            new_data_set.save()

            # Sending csv generation task message.
            generate_csv.s(new_data_set.id).apply_async()

            return HttpResponseRedirect(self.request.path_info)
        else:
            return self.get(request)


def delete_schema(request, schema_id):
    """
    View to delete data schema.
    :param request:
    :param schema_id:
    :return:
    """
    schema = DataSchema.objects.get(pk=schema_id)

    if schema.user == request.user:

        schema.delete()

        return redirect('schema-list')
    else:
        return HttpResponse(status=403)


def download(request, set_id):
    """
    View to download a generated data set.
    :param request:
    :param set_id:
    :return:
    """
    data_set = DataSet.objects.get(pk=set_id)
    if data_set.schema.user == request.user:
        path = settings.MEDIA_ROOT + data_set.file_name

        if os.path.exists(path):
            response = FileResponse(open(path, 'rb'))
            return response

        return HttpResponse(status=404)
    else:
        return HttpResponse(status=403)
