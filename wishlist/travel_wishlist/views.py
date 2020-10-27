from django.shortcuts import render, redirect, get_object_or_404
from .models import Place
from .forms import NewPlaceForm

# Create your views here.

def place_list(request):

    """
    if post request, user clicked add. check if valid, then save
    new place to database and redirect to refresh page for get request
    if nota  post or place isn't valid, display page with list and form to add
    """
    if request.method == "POST":
        form = NewPlaceForm(request.POST)
        place = form.save() # create new place from form
        if form.is_valid(): # check against db constraints
            place.save() # saves to db
            return redirect('place_list') # redirects to get view

    # if not POST or not valid, just render the page
    # with same form and list
    places = Place.objects.filter(visited=False).order_by('name')
    new_place_form = NewPlaceForm
    return render(request, 'travel_wishlist/wishlist.html', { 'places': places, 'new_place_form': new_place_form })

def places_visited(request):
    visited = Place.objects.filter(visited=True)
    return render(request, 'travel_wishlist/visited.html', { 'visited': visited })

def place_was_visited(request, place_pk):
    if request.method == "POST":
        place = get_object_or_404(Place, pk=place_pk)
        place.visited = True
        place.save()
    
    return redirect('place_list')