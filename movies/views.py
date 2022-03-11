from turtle import title
from django.shortcuts import redirect, render
from django.views import View
from django.http import HttpResponse
from django.views.generic import ListView,DetailView
from .models import Movie,Actor,Genre,Rating
from .forms import ReviewForm, RatingForm
from django.db.models import Q
 
class GenreYear:
    def get_genres(self):
        return Genre.objects.all()

    def get_years(self):
        return Movie.objects.filter(draft=False).values("year")

class MoviesView(GenreYear,ListView):
    model = Movie
    queryset = Movie.objects.filter(draft = False)
    paginate_by = 2

    # def get_context_data(self,*args, **kwargs):
    #     context = super().get_context_data(*args,**kwargs)
    #     context["categories"] = Category.objects.all()
    #     return context 
    # template_name = "movies/movie_list.html"
    # context_object_name = "movies"

class MovieDetailView(GenreYear,DetailView):
    model = Movie
    slug_field = "url"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["star_form"] = RatingForm()
        return context

    # def get_context_data(self,*args, **kwargs):
    #     context = super().get_context_data(*args,**kwargs)
    #     context["categories"] = Category.objects.all()
    #     return context  
    # template_name = "movies/movies_detail.html"
    # context_object_name = "movie"
   
class AddReview(GenreYear,View):
    def post(self, request, pk):
        form = ReviewForm(request.POST)
        movie = Movie.objects.get(id=pk)
        if form.is_valid():
            form = form.save(commit=False)
            if request.POST.get("parent", None):
                form.parent_id = int(request.POST.get("parent"))
            form.movie = movie
            form.save()
        return redirect(movie.get_absolute_url())


class ActorView(GenreYear,DetailView):
    model = Actor
    template_name = 'movies/actor.html'
    slug_field = "name"



class FilterMoviesView(GenreYear,ListView):
    def get_queryset(self):
        queryset = Movie.objects.filter(
            Q(year__in=self.request.GET.getlist("year")) |
            Q(genres__in=self.request.GET.getlist("genre"))
            )
        return queryset 



class AddStarRating(View):
    """Добавление рейтинга фильму"""

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

    def post(self, request):
        form = RatingForm(request.POST)
        if form.is_valid():
            Rating.objects.update_or_create(
                ip=self.get_client_ip(request),
                movie_id=int(request.POST.get("movie")),
                defaults={'star_id': int(request.POST.get("star"))}
            )
            return HttpResponse(status=201)
        else:
            return HttpResponse(status=400)


class Search(ListView):
    """Поиск фильмов"""
    paginate_by = 3

    def get_queryset(self):
        return Movie.objects.filter(title__icontains=self.request.GET.get("q"))

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["q"] = f'q={self.request.GET.get("q")}&'
        return context

# movie.get_absolute_url()

# class MovieDetailView(View):
#     def get(self, request, slug):
#         movie = Movie.objects.get(url=slug)
#         return render(request, "movies/movie_detail.html",{"movie":movie})
