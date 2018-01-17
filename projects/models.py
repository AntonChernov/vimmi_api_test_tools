# -*- coding: utf-8 -*-
from django.db import models

from django.utils.translation import ugettext as _

from users.models import User


class Project(models.Model):
    project_name = models.CharField(_('Project name'), max_length=255)
    project_description = models.TextField(_('Description of project'), max_length=1000)
    # project_logo = models.ImageField(upload_to='') # TODO add a image field in sprint 2
    team = models.ManyToManyField(User)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'project'
        verbose_name = 'Project'
        verbose_name_plural = 'Projects'

    def __str__(self):
        return self.project_name

    def get_team_in_project(self, active_team_users_count=False, all_team_users_count=False, active_team_users=False):
        """

        :param active_team_users_count: if set to True
            :return: count of only user with flag is_active==True
        :param all_team_users_count: if set to True
            :return: all users count
        :param active_team_users: if set to True
            :return: list of active users
        :return: list of all users (active and inactive)
        """

        if active_team_users_count and not all_team_users_count and not active_team_users:
            return self.team.all().filter(team_users__user__is_active=True).count()
        elif active_team_users and not active_team_users_count and not all_team_users_count:
            return self.team.all().filter(team_users__user__is_active=True)
        elif all_team_users_count and not active_team_users_count and not active_team_users:
            return self.team.all().count()

        return self.team.all()


