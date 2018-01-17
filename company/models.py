# -*- coding: utf-8 -*-

from django.db import models

from django.utils.translation import ugettext as _

from users.models import User


class Company(models.Model):
    company_name = models.CharField(_('Company name'), max_length=255)
    company_email = models.EmailField(_('Company email'))
    company_owner = models.ForeignKey('User', related_name='owner')
    company_team = models.ManyToManyField('User', related_name='team_users')

    class Meta:
        db_table = 'company'

    def __str__(self):
        return self.company_name

    def get_company_owner(self, obj=True):
        """

        :param obj: get user owner as object(Queryset)
            :return: UserQueryset
        :return: get company user full name if full name has benn set or email otherwise
            :return: Jon Doe or jon_doe@example.com
        """

        if not obj:
            return self.get_company_owner_object().get_full_name()

        return self.company_owner

    def get_company_owner_name(self):
        """
        get company user full name if full name has benn set or email otherwise
        :return: Jon Doe or jon_doe@example.com
        """

    def get_company_team(self, count=False, only_active=False, only_active_count=False):
        """

        :param count: if count variable set to True
            :return: integer count of company users
        :param only_active: if only_active variable set to True
            :return: list of active users in company
        :param only_active_count: if only_active_count variable set to True
            :return: count only active users
        :return: active and inactive users in company
        """

        if count and not only_active and not only_active_count:
            return self.company_team.all().count()
        elif only_active and not count and not only_active_count:
            return self.company_team.filter(is_active=True)
        elif only_active_count and not count and not only_active:
            return self.company_team.filter(is_active=True).count()

        return self.company_team.all()
