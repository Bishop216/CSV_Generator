import random
from django.db import models
from django.contrib.auth.models import User


class DataSchema(models.Model):
    name = models.CharField(max_length=100, null=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


DATA_TYPES = (
    (0, 'Integer'),
    (1, 'Job'),
    (2, 'Email'),
    (3, 'Domain'),
    (4, 'Company')
)


class Column(models.Model):
    name = models.CharField(max_length=100, null=False)
    order = models.IntegerField()
    schema = models.ForeignKey(DataSchema, on_delete=models.CASCADE)
    data_type = models.IntegerField(choices=DATA_TYPES, null=True)
    value_range_from = models.IntegerField(null=True)
    value_range_to = models.IntegerField(null=True)

    def generate_fake_value(self):
        # Integer.
        if self.data_type == 0:
            return random.randint(self.value_range_from, self.value_range_to)

        # Job.
        if self.data_type == 1:
            return random.choice([
                'Project Manager',
                'Lead Developer',
                'QA',
                'SEO',
            ])

        # Email.
        if self.data_type == 2:
            return random.choice([
                'fake@gmail.com',
                'fake.fake@gmail.com',
                'fake.fake.fake@gmail.com',
                'funny.joke@gmail.com',
            ])

        # Domain.
        if self.data_type == 3:
            return random.choice([
                'domain.com',
                'something.com',
                'fake-domain.com',
                'another-one.com',
            ])

        # Company.
        if self.data_type == 4:
            return random.choice([
                'Fake Company',
                'Not Real Services',
                'Something Company',
                'Not A Company',
            ])


class DataSet(models.Model):
    schema = models.ForeignKey(DataSchema, on_delete=models.CASCADE)
    rows = models.IntegerField(null=False, default=10)
    status = models.BooleanField(default=False)
    file_name = models.CharField(max_length=255, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
