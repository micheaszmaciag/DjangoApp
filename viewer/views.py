from django.views.generic import ListView, FormView
from django.urls import reverse_lazy

from viewer.models import Movie
from viewer.forms import MovieForm

from logging import getLogger

LOGGER = getLogger()


class MoviesView(ListView):
    template_name = 'movies.html'
    model = Movie


class MovieCreateView(FormView):
    template_name = 'form.html'
    form_class = MovieForm
    # adres pobrany z URLs na który zostaniemy przekierowani
    # gdy walidacja się powiedzie (movie_create pochodzi z name!)
    success_url = reverse_lazy('movie_create')

    # co ma sie dziać gdy formularz przeszedł walidacje:
    def form_valid(self, form):
        # wywołanie metody form_valid z klasy nadrzędnej (FormView)
        # będziemy zwracać wynik z niej uzyskany
        result = super().form_valid(form)
        # w obiekcie cleaned_data przechowujemy wynik działania
        # funkcji "czyszczących"
        cleaned_data = form.cleaned_data
        # zapisujemy do bazy nowy film:
        Movie.objects.create(
            title=cleaned_data['title'],
            genre=cleaned_data['genre'],
            rating=cleaned_data['rating'],
            released=cleaned_data['released'],
            description=cleaned_data['description'],
        )
        # Zwracamy result - patrz komentarz nad form_valid
        return result

    # co ma sie dziać gdy formularz nie przejdzie walidacji:
    def form_invalid(self, form):
        # odkładamy w logach informacje o operacji
        LOGGER.warning('User provided invalid data')
        # zwracamy wynik działania pierwotnej funkcji form_invalid
        return super().form_invalid(form)
