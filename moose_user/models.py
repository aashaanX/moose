from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.db import models
from randomslugfield.fields import RandomSlugField

from moose import settings

class MooseUserManager(BaseUserManager):
    def create_user(self, user_email, full_name, password):
        """
        :param mobile:
        :param full_name:
        :param gender:
        :param dob:
        :return:
        """

        if not user_email:
            raise ValueError("User must have an email_id")

        if not full_name:
            raise ValueError("User must Provide full name")

        user = self.model(user_email=user_email, full_name=full_name)
        if not password:
            print(user.user_slug)
            password = user.user_slug
        user.set_password(password)
        user.save()
        return user

    def create_staffuser(self, user_email, full_name, password):
        """
        :param user_email:
        :param full_name:
        :param gender:
        :param dob:
        :param password:
        :return:
        """
        user = self.create_user(user_email, full_name, password)
        user.staff = True
        user.save()
        return user


    def create_superuser(self, user_email, full_name, password):
        """
        :param user_email:
        :param full_name:
        :param gender:
        :param dob:
        :param password:
        :return:
        """
        user = self.create_user(user_email, full_name, password)
        user.staff = True
        user.admin = True
        user.save()
        return user



class UserSkill(models.Model):
    """User Skills provided for user; This can be used for asking help and estimate the authentcity of the response"""
    skill_id = models.AutoField(primary_key=True)
    skill_slug = RandomSlugField(length=9)
    skill_name = models.CharField(max_length=50)
    skill_description = models.TextField(null=True, blank=True)

    REQUIRED_FIELDS = ['skill_name']


    class Meta:
        db_table = 'userskills'
        verbose_name_plural = 'User Skills'



class MooseUser(AbstractBaseUser):
    """User Model for authentication porpouse"""
    GENDER = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Others')
    )
    STATUS = (
        ('available', 'available'),
        ('offline', 'offline'),
        ('busy', 'busy'),
        ('snooze', 'snooze')
    )
    user_id = models.AutoField(primary_key=True)
    user_slug = RandomSlugField(length=9)
    user_email = models.CharField(max_length=100, unique=True)
    user_skills = models.ManyToManyField(UserSkill)
    status = models.CharField(max_length=20, choices=STATUS, default='offline')
    full_name = models.CharField(max_length=200)
    about_user = models.TextField(null=True, blank=True)
    gender = models.CharField(max_length=10, choices=GENDER, null=True, blank=True)
    dob = models.DateField(null=True, blank=True)
    active = models.BooleanField(default=True)
    staff = models.BooleanField(default=False)
    admin = models.BooleanField(default=False)

    objects = MooseUserManager()

    USERNAME_FIELD = 'user_email'
    REQUIRED_FIELDS = ['full_name']

    def get_full_name(self):
        return self.full_name

    def get_short_name(self):
        return self.full_name.split(" ")[0]

    def __str__(self):
        return self.user_email + self.status

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.staff

    @property
    def is_active(self):
        return self.active

    @property
    def is_admin(self):
        return self.admin
