import csv
from datetime import datetime
from django.conf import settings
from generator.models import DataSet
from CSV_generator.celery import app


@app.task()
def generate_csv(set_id):
    """
    Celery task to generate a csv file containing fake data.
    :param set_id:
    :return:
    """
    data_set = DataSet.objects.get(pk=set_id)
    schema = data_set.schema
    columns = schema.column_set.order_by('order')

    date = datetime.utcnow().strftime('%Y-%m-%d_%H:%M:%S')
    file_name = schema.name + '_' + date

    with open(settings.MEDIA_ROOT + file_name, 'w') as file:
        writer = csv.writer(file, delimiter=',', quotechar='"')

        writer.writerow([column.name for column in columns])

        for row in range(data_set.rows):
            writer.writerow([column.generate_fake_value() for column in columns])

    data_set.status = True
    data_set.file_name = file_name
    data_set.save()

    return True
