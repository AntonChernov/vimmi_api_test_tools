# -*- coding: utf-8 -*-

from django.shortcuts import render

from users.models import User

from django.views import generic


class CreateUser(generic.CreateView):

    template_name = ''
    queryset = User.objects.all()
