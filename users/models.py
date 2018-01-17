# -*- coding: utf-8 -*-
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser, Group

from django.db import models

from django.utils import timezone
from django.utils.translation import ugettext as _


class CustomUserManager(BaseUserManager):
    def _create_user(self, email, password,
                     is_staff, is_superuser, **extra_fields):
        """
        Create and saves a User with the given email and password.
        """
        now = timezone.now()
        if not email:
            raise ValueError('The given email must be set')
        user = self.model(email=email,
                          is_staff=is_staff, is_active=False,
                          is_superuser=is_superuser, last_login=now,
                          date_joined=now, **extra_fields)

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password, **extra_fields):
        user = self._create_user(email, password, False, False,
                                 **extra_fields)
        user.is_active = True
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        user = self._create_user(email, password, True, True,
                                 **extra_fields)
        user.is_active = True
        user.save()
        return user


class User(AbstractUser):
    email = models.EmailField(_('email address'), unique=True)
    username = models.CharField(_('Username'), max_length=254, null=True, blank=True)
    first_name = models.CharField(_('first name'), max_length=255, blank=True, null=True)
    last_name = models.CharField(_('last name'), max_length=255, blank=True, null=True)
    is_active = models.BooleanField(
        _('active'),
        default=False,
        help_text=_('Designates whether this user should be treated as '
                    'active. Unselect this instead of deleting accounts.'))
    user_is_company = models.BooleanField(default=False)
    company = models.ForeignKey('Company')

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        db_table = 'user'
        verbose_name = _('User')
        verbose_name_plural = _('Users')

    def __str__(self):
        return self.get_full_name()

    def get_full_name(self):
        """
        get full name if set first_name end last_name otherwise returned email
        :return: 'Jon Doe' -> str({first_name} {last_name}).format(first_name, last_name)
        """
        if not self.first_name or not self.last_name:
            return self.email
        return super(User, self).get_full_name()

    def get_user_projects(self, active=False, count_active=False, count_all=False):
        """
        get a list of active projects list for current user
        list(Project1QuerySet, Project2QuerySet, ...)

        :param active: if active set to True
            :return: only active projects

        :param count_active: if count_active set to True
            :return: count of active projects

        :param count_all: if count_all set to True
            :return: count of all projects (active and inactive)

        :return: all project objects related to current user(all project mean active and inactive projects)

        """

        if active and not count_active and not count_all:
            return self.objects.get(id=self.id).project_set.all().filter(is_active=True)
        elif count_active and not active and not count_all:
            return self.objects.get(id=self.id).project_set.all().filter(is_active=True).count()
        elif count_all and not active and not count_active:
            return self.objects.get(id=self.id).project_set.all().count()

        return self.objects.get(id=self.id).project_set.all()

