import os
from django.http import FileResponse, HttpResponse, HttpResponseRedirect
from django.conf import settings
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import DataSet, DataSchema
from .forms import DataSetForm
from .tasks import generate_csv


class DataSchemaList(LoginRequiredMixin, ListView):
    model = DataSchema
    template_name = 'data_schema_list.html'

    def get_queryset(self):
        self.queryset = DataSchema.objects.filter(user=self.request.user)
        return super(DataSchemaList, self).get_queryset()


class DataSetList(LoginRequiredMixin, ListView):
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
