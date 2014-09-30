from django import forms
from projects.models import Role, Project


class RoleEditForm(forms.ModelForm):
    class Meta:
        model = Role
        exclude = ('project',)

class RoleAddForm(forms.ModelForm):
    class Meta:
        model = Role
        fields = ('name',)

class ProjectAddForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ('name',)