# -*- coding: utf-8 -*-
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser

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
    position = models.ForeignKey('Position')
    is_active = models.BooleanField(
        _('active'),
        default=False,
        help_text=_('Designates whether this user should be treated as '
                    'active. Unselect this instead of deleting accounts.'))

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
        if not self.first_name or not self.last_name:
            return self.email
        return super(User, self).get_full_name()


class Position(models.Model):
    position_name = models.CharField(_('Position name'), max_length=255, unique=True)

    def __str__(self):
        return self.position_name

