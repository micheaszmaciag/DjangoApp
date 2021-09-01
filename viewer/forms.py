from django.forms import (
    Form, CharField, IntegerField, ModelChoiceField, DateField, Textarea

)

from viewer.models import Genre



class MovieForm(Form):
    title = CharField(max_length=128) #input - max: 128
    genre = ModelChoiceField(queryset=Genre.objects) #select -> options (pojedynczy wiersz z Genre)
    raiting = IntegerField(min_value=1, max_value=10) #input type: number, min= 1, max=10
    released = DateField() #input type: date
    descrption = CharField(widget=Textarea, required=False) #nie będzie wymaganym polem





