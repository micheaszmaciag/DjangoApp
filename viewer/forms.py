from django.forms import (
    Form, CharField, IntegerField, ModelChoiceField, DateField, Textarea

)

from viewer.models import Genre
from viewer.validators import PastMonthField, capitalized_validator
from django.core.exceptions import ValidationError
import re

class MovieForm(Form):
    title = CharField(max_length=128)  # input - max: 128
    genre = ModelChoiceField(queryset=Genre.objects)  # select -> options (pojedynczy wiersz z Genre)
    rating = IntegerField(min_value=1, max_value=10)  # input type: number, min= 1, max=10
    released = PastMonthField()  # input type: date
    description = CharField(widget=Textarea, required=False)  # nie będzie wymaganym polem


    def clean_descrption(self):
        # pobranie wartości pola description
        initial = self.cleaned_data['descrption']
        # podział tekstu na części "od kropki do kropki" - na zdania
        sentences = re.sub(r'\s*\.\s*','.', initial).split('.')
        # zmiana na wielką literę pierwszej litery każdego ze zdań,
        # dodanie kropki, powtórzenie operacji dla kojnego zadania
        return '. '.join(sentence.capitalize() for sentence in sentences)

    def clean(self):
        result = super().clean()
        if result['genre'].name == 'comedy' and result['rating'] > 7:
            # oznaczenie pola jako błędne bez komentarza
            self.add_error('genre', '')
            self.add_error('rating', '')
            #rzucamy ogólny błąd / wyjątek
            raise ValidationError(
                'Commedies aren\'t so good to be over 7'
            )
        return result
