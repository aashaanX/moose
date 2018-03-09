from django.db import models

class PredictObject(models.Model):
    features = models.ManyToManyField(Feature, related_name='features')
    label = models.ManyToManyField(Label, related_name='label')

class Feature(models.Model):
    name = models.CharField(max_length=50)
    value = models.IntegerField()

class Label(models.Model):
    name = models.CharField(max_length=50)
    value = models.IntegerField