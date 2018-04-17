from django.contrib import admin
from predictor.models import KeyList, Feature, Label, ClassifierMap, ClassifierSet

admin.site.register(KeyList)
admin.site.register(Feature)
admin.site.register(Label)
admin.site.register(ClassifierMap)
admin.site.register(ClassifierSet)
