from django.forms import (
    ModelForm, CharField, IntegerField,

)

from viewer.validators import PastMonthField, capitalized_validator
from django.core.exceptions import ValidationError
from viewer.models import Movie
import re


class MovieForm(ModelForm):
    class Meta: #subklasa opisująca dane z których będzie tworzony formularz
        #model na podstawie którego tworzymy formularz
        model = Movie
        #wykorzystujemy wszystkie pola z modelu
        fields = '__all__'

    #pola z własnymi walidatorami dodajemy oddzielnie poza META
    title = CharField(validators=[capitalized_validator])
    rating = IntegerField(min_value=1, max_value=10)
    released = PastMonthField()

    def clean_descrption(self):
        # pobranie wartości pola description
        initial = self.cleaned_data['descrption']
        # podział tekstu na części "od kropki do kropki" - na zdania
        sentences = re.sub(r'\s*\.\s*', '.', initial).split('.')
        # zmiana na wielką literę pierwszej litery każdego ze zdań,
        # dodanie kropki, powtórzenie operacji dla kojnego zadania
        return '. '.join(sentence.capitalize() for sentence in sentences)

    def clean(self):
        result = super().clean()
        if result['genre'].name == 'comedy' and result['rating'] > 7:
            # oznaczenie pola jako błędne bez komentarza
            self.add_error('genre', '')
            self.add_error('rating', '')
            # rzucamy ogólny błąd / wyjątek
            raise ValidationError(
                'Commedies aren\'t so good to be over 7'
            )
        return result
