from django.forms import forms
from .model import Label


class LabelCreateForm(form.ModelForm):
    class Meta:
        model = Label
        fields = ["name"]
        labels = {
            "name": "Имя",
        }