# -*- coding: utf-8 -*-

from django import forms

from users.models import User


class CreateUserForm(forms.Form):
    password = forms.EmailField(max_length=12, min_length=6)
    email = forms.EmailField()
    first_name = forms.CharField(max_length=255)

    def save(self, commit=True):
        password = self.cleaned_data.pop('password')
        user = User.objects.create_user(**self.cleaned_data)
        user.set_password()
