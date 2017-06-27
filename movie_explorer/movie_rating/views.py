import datetime
import tmdbsimple as tmdb

from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.db.utils import DatabaseError
from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.views.generic import TemplateView
from django.views.generic import ListView
from .models import MovieRatings, MovieComments
from django.shortcuts import get_object_or_404
from django.http import Http404
import requests
from django.db.models import Avg
from django.template import RequestContext
from operator import itemgetter

# For UserModelEmailBackend
from django.contrib.auth.hashers import check_password
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend

# Create your views here.
class MovieView(TemplateView):
    tmdb.API_KEY = settings.TMDB_API_KEY
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        try:
            movies = tmdb.Movies()
            config = tmdb.Configuration().info()
            POSTER_SIZE = 2

            context = {}
            context['status'] = 'success'
            context['results'] = movies.top_rated(page = 1)['results'][:10]
            context['image_path'] = config['images']['base_url'] + config['images']['poster_sizes'][POSTER_SIZE]
            return context
        except (requests.exceptions.HTTPError, tmdb.APIKeyError )as e:
            context = {}
            print ("THE API IS WRONG")
            context["status"] = 'failure'
            return context

class MovieDescriptionView(TemplateView):
    tmdb.API_KEY = settings.TMDB_API_KEY
    template_name = 'description.html'

    def get_context_data (self, **kwargs):
        movieID = self.kwargs['tmdb_movie_id']
        context = {}
        try:
            current_user = self.request.user
            movies = tmdb.Movies(int(movieID))
            config = tmdb.Configuration().info()
            POSTER_SIZE = 3

            context['status'] = 'success'
            context['results'] =  movies.info()
            context['image_path'] = config['images']['base_url'] + config['images']['poster_sizes'][POSTER_SIZE]
            #Get average rating from the DB
            context['rating'] = MovieRatings.objects.all().filter(movie_id = int(movieID)).aggregate(Avg('rating'))
            if context['rating']['rating__avg'] is not None:
                context['rating_formatted'] = "{:.2f}".format(context['rating']['rating__avg'])

            context['videos'] = movies.videos()
            # context['video_link'] = "https://www.youtube.com/watch?v=" + context['videos']['results'][0]['key']
            context['video_link'] = ""
            context['video_link_emb'] = ""
            for x in context['videos']['results']:
                if x['type'] == "Trailer":
                    context['video_link'] = "https://www.youtube.com/watch?v=" + x['key']
                    context['video_link_emb'] = "https://www.youtube.com/embed/" + x['key']
                    break
            if context['video_link'] == "":
                context['video_link'] = "No Trailer Found"
                # context['video_link'] = context['videos']['results']

            context['genre'] = []
            for x in context['results']['genres']:
                context['genre'].append(x['name'])
            # context['title'] = context['results']['original_title']

            #Show stars
            if current_user.is_authenticated:
                try:
                    m = MovieRatings.objects.get(user=current_user, movie_id=movies.id)
                    rating = m.rating
                except:
                    rating = 0
                context['current_rating'] = str(rating)

            #Show comments
            try:
                c = MovieComments.objects.filter(movie_id=movies.id).all()
            except DatabaseError:
                print ("Unable to access database.")
            
            context['comments']=c

            #Similar movies
            similar_movies = movies.similar_movies(page =1 ) #only show one page :(
            if similar_movies['total_results'] == 0:
                context['similar'] = None
            else :
                context['similar'] = similar_movies['results']

            return context

        except (requests.exceptions.HTTPError, tmdb.APIKeyError)as e:
            context = {}
            print ("THE API IS WRONG")
            context["status"] = 'failure'
            return context

    @staticmethod
    def post(request, *args, **kwargs):
        context_instance = RequestContext(request)
        action = request.POST.get('action', '')
        if action == "rate_movie":
            # get important info
            movieID = int(request.POST['movie_id'])
            rating_given = int(request.POST['rating'])
            current_user = request.user
            updated = False

            if current_user.is_authenticated:
                try:
                    movie = MovieRatings.objects.get(user=current_user, movie_id=movieID)
                    # update rating
                    movie.rating = int(rating_given)
                    movie.save()
                    updated = True
                except MovieRatings.DoesNotExist:
                    MovieRatings.objects.create(user=current_user, movie_id=movieID, rating=rating_given)
                    updated = True

            res = {}
            if updated:
                res['status'] = 'success'
                res['current_rating'] = str(rating_given)
                res['rating'] = MovieRatings.objects.all().filter(movie_id=int(movieID)).aggregate(Avg('rating'))
                return render(request, 'description.html', res )
            else:
                res['status'] = 'failure'
                return render(request, 'description.html', res )


        elif action == "add_comment":

            movieID = int(request.POST['movie_id'])
            comment_given = str(request.POST['comment'])
            current_user = request.user
            updated = False

            if current_user.is_authenticated:
                try:
                    MovieComments.objects.create(user=current_user, movie_id=movieID, comment=comment_given)
                    updated = True
                except DatabaseError:
                    print ("Error in database. Unable to add comment")

            res = {}
            if updated:
                res['status'] = 'success'
                res['comments'] = MovieComments.objects.all().filter(movie_id=int(movieID))
                return render(request, 'description.html', res)
                # reload newly added comments
            else:
                res['status'] = 'failure'
                return render(request, 'description.html', res)
        
            
        return render(request, 'description.html', {} )

class MyRatingsView(TemplateView):
    tmdb.API_KEY = settings.TMDB_API_KEY
    template_name = 'myratings.html'

    def get_context_data(self, **kwargs):
        context = {'page_type': 'myrating_page'}
        myratings = []
        try:
            data_entries = MovieRatings.objects.filter(user=self.request.user)

            for entry in data_entries:
                movie = tmdb.Movies(int(entry.movie_id))
                config = tmdb.Configuration().info()
                POSTER_SIZE = 1
                myratings.insert(0, (movie.info(), entry.rating,
                                     config['images']['base_url'] + config['images']['poster_sizes'][POSTER_SIZE]))

            if self.request.user.is_authenticated:
                if not myratings:
                    context['status'] = 'failure'
                else:
                    context['status'] = 'success'
                    context['results'] = myratings

            return context

        except (requests.exceptions.HTTPError, tmdb.APIKeyError)as e:
            context = {}
            print ("API ERROR")
            context["status"] = 'failure'
            return context

    @staticmethod
    def post(request, *args, **kwargs):
        context_instance = RequestContext(request)
        action = request.POST.get('action', '')
        if action == "rate_movie":
            # get important info
            movieID = int(request.POST['movie_id'])
            rating_given = int(request.POST['rating'])
            current_user = request.user
            updated = False
            context = {}

            if current_user.is_authenticated:
                try:
                    movie = MovieRatings.objects.get(user=current_user, movie_id=movieID)

                    if rating_given == 0:
                        movie.delete()
                    else:
                        # update rating
                        movie.rating = int(rating_given)
                        movie.save()
                    updated = True
                except MovieRatings.DoesNotExist:
                    MovieRatings.objects.create(user=current_user, movie_id=movieID, rating=rating_given)
                    updated = True

                myratings=[]

                try:
                    data_entries = MovieRatings.objects.filter(user=request.user)

                    for entry in data_entries:
                        movie = tmdb.Movies(int(entry.movie_id))
                        config = tmdb.Configuration().info()
                        POSTER_SIZE = 1
                        myratings.insert(0, (movie.info(), entry.rating,
                                             config['images']['base_url'] + config['images']['poster_sizes'][
                                                 POSTER_SIZE]))

                    if not myratings:
                        context['status'] = 'failure'
                    else:
                        context['status'] = 'success'
                        context['results'] = myratings

                except (requests.exceptions.HTTPError, tmdb.APIKeyError)as e:
                    context["status"] = 'failure'

            return render(request, 'myratings.html', context)

        return render(request, 'myratings.html', {})

def register(request):
    """ Handle registration form """
    if request.method == 'POST':
        response = dict(
            errors=list(),
        )
        # This field firstname and lastname are disable
        #  for first sprint and should be enable back in the second sprint.

        # first_name = request.POST['first_name']
        # last_name = request.POST['last_name']
        email = request.POST['email']
        username = request.POST['username']
        password = request.POST['password']
        confirm_pwd = request.POST['confirm_pwd']

        #   Check if the fields are not empty

        # if not first_name.strip():
        #     response['errors'].append(' Please fill in your first name.')
        # if not last_name.strip():
        #     response['errors'].append(' Please fill in your last name.')

        if not email.strip():
            response['errors'].append(' Please fill in your email address.')
        if not username.strip():
            response['errors'].append(' Please fill in your username.')
        if not password:
            response['errors'].append(' Please fill in your password.')
        if not confirm_pwd:
            response['errors'].append(' Please confirm your password.')

        # Check if both passwords are matched
        if password != confirm_pwd:
            response['errors'].append(' Passwords do not match.')

        # Check if  username is unique
        try:
            user = User.objects.get(username=username)
            response['errors'].append(' Username is already in use.')
        except User.DoesNotExist:
            pass

        # Check if Email is unique
        try:
            user = User.objects.get(email=email)
            response['errors'].append(' Email is already in use.')
        except User.DoesNotExist:
            pass

        # Check if the Email is valid format
        try:
            validate_email(email)
        except ValidationError:
            response['errors'].append(' Email is not in correct format')

        if response['errors']:
            return render(request, 'register.html', response)
        else:
            # Store the new user into the database

            # User.objects.create_user(username,
            #                          email=email,
            #                          password=password,
            #                          last_name=last_name,
            #                          first_name=first_name)

            # Once you enable firstname and lastname fields, please remove bellowed object.
            User.objects.create_user(username,
                                     email=email,
                                     password=password)
            response['success'] = 'You are successfully registered to Movie Explorer!'
            return render(request, 'register.html', response)

    else:
        return render(request, 'register.html')

class UserModelEmailBackend(ModelBackend):

    def authenticate(self, username="", password="", **kwargs):
        try:
            user = get_user_model().objects.get(email__iexact=username)
            if check_password(password, user.password):
                return user
            else:
                return None
        except get_user_model().DoesNotExist:
            # No user was found, return None - triggers default login failed
            return None

def search(request):
    
    # Set the page to search
    context = {'page_type': 'search_page'}

    """ Handle registration form """
    if request.method == 'POST':
        response = dict(
            errors=list(),
        )

        search_query = request.POST['search']

        try:
            sort_option = request.POST['search_sort_by']
        except:
            sort_option = 'popularity.desc'
        context['sort_selected'] = sort_option

        # Convert sort_option
        if (sort_option == 'release_date.desc'):
            sort_by = 'release_date'
            reversed = True
        elif (sort_option == 'release_date.asc'):
            sort_by = 'release_date'
            reversed = False
        else:
            sort_by = 'popularity'
            reversed = True

        # Check if query is empty
        if len(search_query) == 0:
            context['status'] = 'empty'
            return render(request, 'home.html', context)

        else:
            tmdb.API_KEY = settings.TMDB_API_KEY
            
            # Query the API
            try:
                search = tmdb.Search()
                config = tmdb.Configuration().info()
                POSTER_SIZE = 2

                context['search'] = search_query

                context['status'] = 'success'

                # ------ Sort Results ----------
                cur_page = 1
                results_list = []
                while (cur_page <= 5):
                    movie_query = search.movie(page=cur_page, query=search_query)

                    # get necessary info and put into list of tuples
                    for r in search.results:
                        results_list += [(r['id'], r['poster_path'], r['title'], r[sort_by])]
                    cur_page += 1
                # sort
                results_sorted = sorted(results_list, key=itemgetter(3), reverse=reversed)

                # back to dict
                results_dict = []
                for i in results_sorted:
                    results_dict += [{'id': i[0], 'poster_path': i[1], 'title': i[2]}]

                context['results'] = results_dict

                context['image_path'] = config['images']['base_url'] + config['images']['poster_sizes'][POSTER_SIZE]

                if len(context['results']) == 0:
                    context['status'] = 'noresult'

                return render(request, 'home.html', context)

            except (requests.exceptions.HTTPError, tmdb.APIKeyError )as e:
                print ("THE API IS WRONG")
                context["status"] = 'failure'
                return render(request, 'home.html', context)
                
    else:
        return render(request, 'home.html')

# ----This is goes to the home page----
# This is function does both sort and filter together
def sort(request):
    sort_option = 'popularity.desc'
    genre_option = ''
    page = '1'
    context = {'page_type' : 'sort_and_filter'}
    tmdb.API_KEY = settings.TMDB_API_KEY

    try:
        discover = tmdb.Discover()
        config = tmdb.Configuration().info()
        POSTER_SIZE = 2

        if request.method == 'POST':
            context['status'] = 'success'
            sort_option = request.POST['sort_by']
            genre_option = request.POST['genre']

            if request.POST.__contains__('prev_page'):
                page = request.POST.get('prev_page', '2')
                pageNumber = int(page)
                page = str(pageNumber - 1)
            elif request.POST.__contains__('next_page'):
                page = request.POST.get('next_page', '0')
                pageNumber = int(page)
                page = str(pageNumber + 1)
            else:
                page = '1'

        movie_query = discover.movie(page=page, sort_by=sort_option, with_genres=genre_option, with_release_type='2|3|4|5|6')
        # For testing purposes, you can use commented query below to get result which will only return 2 pages
        # movie_query = discover.movie(page=page, sort_by=sort_option, with_genres=genre_option, vote_count_gte='6234')

        context['results'] = movie_query['results']

        context['last_page'] = 'false'
        if int(page) == movie_query['total_pages']:
            context['last_page'] = 'true'

        if len(context['results']) == 0:
            context['status'] = 'noresult'

        context['image_path'] = config['images']['base_url'] + config['images']['poster_sizes'][POSTER_SIZE]
        context['sort_selected'] = sort_option
        context['genre_selected'] = genre_option
        context['page_num'] = page
        return render(request, 'home.html', context)

    except (requests.exceptions.HTTPError, tmdb.APIKeyError)as e:
        print("THE API IS WRONG")
        context["status"] = 'failure'
        return render(request, 'home.html', context)

def viewRatings(request):
    context = {'page_type': 'myrating_page'}
    myratings = []
    if request.method == 'POST':
        response = dict(
            errors=list(),
        )
        tmdb.API_KEY = settings.TMDB_API_KEY

        data_entries = MovieRatings.objects.filter(user=request.user)

        for entry in data_entries:
            movie = tmdb.Movies(int(entry.movie_id))
            config = tmdb.Configuration().info()
            POSTER_SIZE = 1
            myratings.insert(0, (movie.info(), entry.rating, config['images']['base_url'] + config['images']['poster_sizes'][POSTER_SIZE]))

        if request.user.is_authenticated:
            if not myratings:
                context['status'] = 'failure'

            else:
                context['status'] = 'success'
                context['results'] = myratings

        return render(request, 'myratings.html', context)

    else:
        raise Http404("No Movie Selected")

def changePass(request):
    if request.user.is_authenticated:
        """ Handle change password form """
        if request.method == 'POST':
            response = dict(
                errors=list(),
            )
            oldPass = request.POST['oldPass']
            newPass = request.POST['newPass']
            confirmPass = request.POST['confirmPass']

            #   First check if the fields are not empty
            if not oldPass:
                response['errors'].append(' Please fill in your old password.')
            if not newPass:
                response['errors'].append(' Please fill in your new password.')
            if not confirmPass:
                response['errors'].append(' Please confirm your password.')

            # If any are empty, return errors immediately
            if response['errors']:
                return render(request, 'changePassword.html', response)

            # Next, check if old password is correct
            if not request.user.check_password(oldPass):
                response['errors'].append(' Your password is incorrect. Try again.')

            # Check if new passwords match
            if newPass != confirmPass:
                response['errors'].append(' New Password and Confirm Password do not match.')

            if response['errors']:
                return render(request, 'changePassword.html', response)
            elif oldPass == newPass:
                response['noChange'] = 'New Password is the same as Old Password'
                return render(request, 'profile.html', response)
            else:
                # Set the new password
                user = request.user
                user.set_password(newPass)
                user.save()
                response['success'] = 'You password has been changed :)'

                # Log user back in (since this logged them out)
                login(request, user, backend=settings.AUTHENTICATION_BACKENDS[0])

                return render(request, 'profile.html', response)

        else:
            return render(request, 'changePassword.html')
    else:
        return redirect('//')

def profile(request):
    if request.user.is_authenticated:
        return render(request, 'profile.html')
    else:
        return redirect('//')