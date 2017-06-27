from django.contrib import admin
from .models import  MovieRatings, MovieComments

# Register your models here.
admin.site.register(MovieRatings)
admin.site.register(MovieComments)
