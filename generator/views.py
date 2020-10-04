import os
from django.http import FileResponse, HttpResponse
from django.conf import settings
from .models import DataSet


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

