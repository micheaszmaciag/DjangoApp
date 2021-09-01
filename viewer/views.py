from django.shortcuts import render
from django.http import  HttpResponse
from django.views import View
from viewer.models import Movie
# Create your views here.



class MoviesView(View):
    def get(self, request):
        return render(
            request, template_name='movies.html',
            context={
                'movies': Movie.objects.all()
            }
        )

