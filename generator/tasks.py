import csv
from datetime import datetime
from django.conf import settings
from generator.models import *
from CSV_generator.celery import app


@app.task()
def generate_csv(schema_id, rows):
    """
    Celery task to generate a csv file containing fake data.
    :param schema_id:
    :param rows:
    :return:
    """
    schema = DataSchema.objects.get(pk=schema_id)
    columns = schema.column_set.order_by('order')
    date = datetime.utcnow().strftime('%Y-%m-%d_%H:%M:%S')

    with open(settings.MEDIA_ROOT + schema.name + '_' + date, 'w') as file:
        writer = csv.writer(file, delimiter=',', quotechar='"')

        writer.writerow([column.name for column in columns])

        for row in range(rows):
            writer.writerow([column.generate_fake_value() for column in columns])

    return True
