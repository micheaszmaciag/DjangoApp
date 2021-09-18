from django.contrib import admin
from django.contrib.admin import ModelAdmin


# Register your models here.

class MovieAdmin(ModelAdmin):

    @staticmethod
    def released_year(obj):
        return obj.released.year

    @staticmethod
    def cleanup_description(modeladmin, request, queryset):
        queryset.update(description=None)

    ordering = ['id'] #sortowanie po ID,
    #jakie kolumny mają zostać wyświetlone (released_year to wynik działania
    #funkcji realeased_year zdefiniowanej w 9 linijce)
    list_display = ['id','title', 'genre', 'released_year']
    #po kliknięciu na jakie komórki mamy zostać przerzuceni do edycji
    list_display_links = ['id', 'title']
    #paginacja - liczba wierszy na jedną stronę, później meny z wyborem
    # kolejnej strony (jak w wynikach wyszukiwania google)
    list_per_page = 20
    # dodatkowy panel z filtrami
    list_filter = ['genre']
    #dodatkowe pole do szukania po tekście
    search_fields = ['title']
    #dodatkowe akcje - cleanup_description zdefiniowałem w 13 linijce
    actions = ['cleanup_description']

    #konfiguracja formularza edycji
    fieldsets = [
        # każda z sekcji podzielona krotką
        #pierwsza wartość krotki to nagłówek sekcji
        #druga wartość krotki to słownik z konfiguracją
        (None, {'fileds': ['title', 'created']}),
        #External information - nagłówek sekcji (przykład)
        ('External information', {
            #klucz fields przechowuje listę nazw pól które mają zostać
            #zaprezentowane w sekcji
            'fileds': ['genre', 'released'],
            #klucz description to opis sekcji
            'description': 'This fields are external information!'
        }),
        ('User information'), {
            'fields': ['rating','description'],
            'description': 'This fields will be filled with user.'
        }

    ]
    #lista nazw pól tylko do odczytu
    readonly_fields = ['created']




