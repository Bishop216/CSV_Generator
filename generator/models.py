import random
from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class DataSchema(models.Model):
    name = models.CharField(max_length=100, null=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Column(models.Model):
    name = models.CharField(max_length=100, null=False)
    order = models.IntegerField()


# Data types.

class Integer(models.Model):
    range_from = models.IntegerField()
    range_to = models.IntegerField()
    column = models.OneToOneField(Column, on_delete=models.CASCADE)

    def generate_fake_value(self):
        return random.randint(self.range_from, self.range_to)


class Job(models.Model):
    column = models.OneToOneField(Column, on_delete=models.CASCADE)

    @staticmethod
    def generate_fake_value():
        return random.choice([
            'Project Manager',
            'Lead Developer',
            'QA',
            'SEO',
        ])


class Email(models.Model):
    column = models.OneToOneField(Column, on_delete=models.CASCADE)

    @staticmethod
    def generate_fake_value():
        return random.choice([
            'fake@gmail.com',
            'fake.fake@gmail.com',
            'fake.fake.fake@gmail.com',
            'funny.joke@gmail.com',
        ])


class DomainName(models.Model):
    column = models.OneToOneField(Column, on_delete=models.CASCADE)

    @staticmethod
    def generate_fake_value():
        return random.choice([
            'domain.com',
            'something.com',
            'fake-domain.com',
            'another-one.com',
        ])


class PhoneNumber(models.Model):
    column = models.OneToOneField(Column, on_delete=models.CASCADE)

    @staticmethod
    def generate_fake_value():
        return random.choice([
            '+380-311-8555-52',
            '+380-635-5559-18',
            '+380-109-6555-50',
            '+380-261-6555-63',
        ])


class CompanyName(models.Model):
    column = models.OneToOneField(Column, on_delete=models.CASCADE)

    @staticmethod
    def generate_fake_value():
        return random.choice([
            'Fake Company',
            'Not Real Services',
            'Something Company',
            'Not A Company',
        ])
