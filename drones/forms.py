from django import forms

from django.contrib.auth import get_user_model

from django.contrib.auth.forms import UserCreationForm

from django.forms import DateInput

from drones.models import Worker, Task


#  Adding/Editing Tasks
class TaskForm(forms.ModelForm):
    assignees = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="Assign workers"
    )

    class Meta:
        model = Task
        fields = "__all__"
        widgets = {
            "deadline": DateInput(attrs={"type": "date"})
        }


#  Search forms
class TaskSearchForm(forms.Form):
    q = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(attrs={"placeholder": "Search by task"}),
    )


class WorkerSearchForm(forms.Form):
    q = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(attrs={"placeholder": "Search by worker"}),
    )


class PositionSearchForm(forms.Form):
    q = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(attrs={"placeholder": "Search by position"}),
    )


class TaskTypeSearchForm(forms.Form):
    q = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(attrs={"placeholder": "Search by task type"}),
    )


#  Worker registration form
class WorkerCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Worker
        fields = UserCreationForm.Meta.fields + (
            "first_name",
            "last_name",
            "email",
            "position",
        )
