from django.db.models import Q, Count
from django.http import HttpRequest
from datetime import datetime
from app.forms import AddReviewForm, SignUpForm, EditProfile
from app.models import Review, User
from django.db.models import Avg
from django.http import HttpResponseNotFound
from django.http import HttpResponseRedirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.contrib.auth.models import User as uu

from app.forms import MediaInsertForm, AuthorInsertForm, SearchData
from app.models import Media, MediaAuthor


def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)

    best_reviews = Review.objects.values("media_id").annotate(
        the_count=Count("media_id")
    ).order_by(
        "-the_count"
    )[:9]

    if len(best_reviews) > 8:
        movies = Media.objects.filter(id__in=best_reviews.values("media_id"))
    else:
        movies = Media.objects.all()[:9]

    form = SearchData(request.POST or None)
    if 'Search' in request.POST:
        search = request.POST
        if search["Search"]:

            query = Media.objects.filter(
                    Q(name__contains=search["Search"]))
            print(query)
            return render(request, 'index.html', {'form': form, 'posts': query})
        else:
            return render(request, 'index.html', {'error': True, 'form': form})
    else:
        return render(request, 'index.html', {'error': False, 'form': form, 'posts': movies})


def reviews(request):
    """Renders the contact page."""
    assert isinstance(request, HttpRequest)

    media_id = request.GET.get('mediaid', '')

    # if there are no attributes return not found
    if media_id == "":
        return HttpResponseNotFound("Not found")

    review_list = Review.objects.filter(media=media_id)
    media = Media.objects.get(id=media_id)
    avg_rating = Review.objects.filter(media=media_id).aggregate(Avg("rate"))

    # Get the number of 1 2 3 4 5 STARS
    one_star, two_stars, three_stars, four_stars, five_stars = 0, 0, 0, 0, 0

    for sm in review_list:
        if sm.rate == 1:
            one_star += 1
        elif sm.rate == 2:
            two_stars += 1
        elif sm.rate == 3:
            three_stars += 1
        elif sm.rate == 4:
            four_stars += 1
        elif sm.rate == 5:
            five_stars += 1

    # get the distribution of the percentages
    distros = make_distributions(review_list.count(), five_stars, four_stars, three_stars, two_stars, one_star)

    tparams = {
        'reviews': review_list,
        'media': media,
        'one': one_star,
        'two': two_stars,
        'three': three_stars,
        'four': four_stars,
        'five': five_stars,
        'avg': 0 if avg_rating['rate__avg'] is None else round(avg_rating['rate__avg']),
        'distros': distros
    }

    if request.method == 'POST':

        form = AddReviewForm(request.POST)
        if form.is_valid():

            review = form.cleaned_data['review']
            rate = form.cleaned_data['rate']
            # ADD TO DB

            """
                PROBLEM:
                NEEDS A USER
                WHEN WE REGISTER IT DOENSN'T CREATE A USER IN THE DB BUT IN AUTHENTICATION
            
            """

            new_review = Review.objects.create(author=User.objects.get(authentication_id=uu.objects.get(username=request.user).id),
                                           media=Media.objects.get(id=media_id), rate=rate, review=review)
            new_review.save()

            tparams = {
                'reviews': reviews,
                'form': form,
                'one': one_star,
                'two': two_stars,
                'three': three_stars,
                'four': four_stars,
                'five': five_stars,
                'avg': 0 if avg_rating['rate__avg'] is None else round(avg_rating['rate__avg']),
                'distros': distros
            }
            return HttpResponseRedirect('/reviews/?mediaid=' + str(media_id))
    else:
        form = AddReviewForm()
        tparams = {
            'reviews': review_list,
            'media': media,
            'form': form,
            'one': one_star,
            'two': two_stars,
            'three': three_stars,
            'four': four_stars,
            'five': five_stars,
            'avg': 0 if avg_rating['rate__avg'] is None else round(avg_rating['rate__avg']) ,
            'distros': distros
        }
    return render(request, 'reviews.html', tparams)


def about(request):
    assert isinstance(request, HttpRequest)
    tparams = {
        'title': 'About',
        'message': 'Your application description page.',
        'year': datetime.now().year,
        'isadmin': True,
    }
    return render(request, 'about.html', tparams)


def add_media_page(request):
    #if not request.user.is_authenticated or request.user.username != 'admin':
    #    return redirect('/login')

    form = MediaInsertForm(request.POST, request.FILES)

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return render(request, 'addmedia.html', {'inserted': form.cleaned_data["name"], 'form': form})
        else:
            return render(request, 'addmedia.html', {'error': True, 'form': form})
    else:
        return render(request, 'addmedia.html', {'error': False, 'form': form})


def add_author_page(request):
    form = AuthorInsertForm(request.POST, request.FILES)

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return render(request, 'addauthor.html', {'inserted': form.cleaned_data["name"], 'form': form})
        else:
            return render(request, 'addauthor.html', {'error': True, 'form': form})
    else:
        return render(request, 'addauthor.html', {'error': False, 'form': form})


def search(request):

    form = SearchData(request.POST)
    if 'Search' in request.POST:
        search = request.POST
        if search["Type"] and search["Search"]:
            if search["Type"] == "1":
                query = Media.objects.filter(Q(name__contains=search["Search"]) | Q(description__contains=search["Search"]))

            else:
                query = MediaAuthor.objects.all()
            print("Type is: " + str(search["Type"]))
            print("Search: " + str(search["Search"]))
            print("Query: " + str(query))
            return render(request, 'search.html', {'query': query, 'form': form})
        else:
            return render(request, 'search.html', {'error': True, 'form': form})
    else:
        return render(request, 'search.html', {'error': False, 'form': form})




# Make distributions
def make_distributions(number_total, five, four, three, two, one):
    if number_total == 0:
        return {'five_perc': 0,
             'four_perc': 0,
             'three_perc': 0,
             'two_perc': 0,
             'one_perc': 0
             }
    else:
        return {'five_perc': (five / number_total) *100,
             'four_perc': (four / number_total) *100,
             'three_perc': (three / number_total) *100,
             'two_perc': (two / number_total) *100,
             'one_perc': (one / number_total) *100
             }

def register(request):

    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()

            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            user_profile = User(authentication_id=user.id)
            user_profile.save()
            login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'register.html', {'form': form})


def userprofile(request):

    user_id = request.GET.get('userid', '')

    the_user = User.objects.get(id=user_id)

    reviews = Review.objects.filter(author_id=user_id)

    print(request.POST)
    print(request.method)

    form = EditProfile(request.POST, request.FILES)
    if request.method == 'POST':

        print(form.errors)
        if form.is_valid():
            print(request.FILES)
            usr = the_user
            usr.img = request.FILES["img"]
            usr.save()
    try:

        print("request.user: " + str(request.user))
        print("User get: " + the_user.authentication.username)

        form = EditProfile if str(request.user) == str(the_user.authentication.username) else ''
    except User.DoesNotExist:
        form = ''

    if user_id:
        return render(request, 'userprofile.html', {'user': the_user, 'reviews': reviews, 'editform': form})
    else:
        return render(request, 'userprofile.html', {})
