from rest_framework import generics
from django_filters.rest_framework import DjangoFilterBackend

from .models import *
from .serializers import (
MovieListSerializers, MovieDetailSerializers, 
ReviewCreateSerializer, CreateRatingSerializer,
ActorListSerializer, ActorDetailSerializer)
from .service import get_client_ip, MovieFilter


class MovieListView(generics.ListAPIView):
    # Вывод списка фильмов
    serializer_class = MovieListSerializers
    filter_backends = (DjangoFilterBackend,)
    filterset_class = MovieFilter
    
    def get_queryset(self):
        movies = Movie.objects.filter(draft=False).annotate(
            rating_user=models.Count("ratings", filter=models.Q(ratings__ip=get_client_ip(self.request)))
        ).annotate(
            middle_star=models.Sum(models.F('ratings__star')) / models.Count(models.F('ratings'))
        )
        return movies

# class MovieListView(APIView):
#     def get(self, request):
#         movies = Movie.objects.filter(draft=False).annotate(
#             rating_user=models.Count("ratings", filter=models.Q(ratings__ip=get_client_ip(request)))
#         ).annotate(
#             middle_star=models.Sum(models.F('ratings__star')) / models.Count(models.F('ratings'))
#         )
#         serializer = MovieListSerializers(movies, many=True)
#         return Response(serializer.data)



class MovieDetailView(generics.RetrieveAPIView):
        queryset = Movie.objects.filter(draft=False)
        serializer_class = MovieDetailSerializers

class ReviewCreateView(generics.CreateAPIView):
    serializer_class = ReviewCreateSerializer
       

class AddStarRatingView(generics.CreateAPIView):
    # Добавление рейтинга фильму
    serializer_class = CreateRatingSerializer
    def perform_create(self, serializer):
        serializer.save(ip=get_client_ip(self.request))
      


class ActorListView(generics.ListAPIView):
    queryset = Actor.objects.all()
    serializer_class = ActorListSerializer


class ActorDetailView(generics.RetrieveAPIView):
    queryset = Actor.objects.all()
    serializer_class = ActorDetailSerializer