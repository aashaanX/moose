from django.db import models

from moose_user.models import MooseUser


class KeyList(models.Model):
    name = models.CharField(max_length=50)
    created_user = models.ForeignKey(MooseUser, related_name='user', on_delete=models.CASCADE)
    key_type = models.CharField(max_length=50, choices=(('Label', 'Label'), ('Feature', 'Feature')))

    def __str__(self):
        return self.name + "|" + self.key_type


class Feature(models.Model):
    name = models.CharField(max_length=50)
    value = models.IntegerField()
    created_user = models.ForeignKey(MooseUser, on_delete=models.CASCADE)

    def __str__(self):
        return self.name + "|" + str(self.value) + "|" + self.created_user.full_name

    def save(self, *args, **kwargs):
        """
        Method to save the feature
        :param args:
        :param kwargs:
        :return:
        """
        if not self.pk:
            if self.name in KeyList.objects.filter(key_type='Feature'):
                # if name in key list of features add feature
                super(Feature, self).save(args, kwargs)
            else:
                if self.created_user.staff or self.created_user.admin:
                    # if not in key list feature and created user is staff or admin
                    key_value = KeyList()
                    key_value.name = self.name
                    key_value.key_type = "Feature"
                    key_value.created_user = self.created_user
                    key_value.save()
                    super(Feature, self).save(args, kwargs)
                else:
                    raise ValueError("User not Authorised")
        else:
            raise ValueError("primary Key Exist")


class Label(models.Model):
    name = models.CharField(max_length=50)
    value = models.IntegerField()
    created_user = models.ForeignKey(MooseUser, on_delete=models.CASCADE)

    def __str__(self):
        return self.name + "|" + str(self.value) + "|" + self.created_user.full_name

    def save(self, *args, **kwargs):
        if not self.pk:
            if self.name in KeyList.objects.filter(key_type='Label'):
                super(Label, self).save(args, kwargs)
            else:
                if self.created_user.staff or self.created_user.admin:
                    key_value = KeyList()
                    key_value.name = self.name
                    key_value.key_type = "Label"
                    key_value.created_user = self.created_user
                    key_value.save()
                    super(Label, self).save(args, kwargs)
                else:
                    raise ValueError("User not Authorised")
        else:
            raise ValueError("primary Key Exist")


class ClassifierMap(models.Model):
    features = models.ManyToManyField(Feature, related_name='features')
    label = models.ForeignKey(Label, related_name='label', on_delete=models.CASCADE)
    created_user = models.ForeignKey(MooseUser, on_delete=models.CASCADE, related_name='created_user')

    def __str__(self):
        return self.label.name + "|" + str(self.features)


class ClassifierSet(models.Model):
    name = models.CharField(max_length=50)
    classifier_map = models.ManyToManyField(ClassifierMap)

    def __str__(self):
        return self.name
