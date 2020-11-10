from django.shortcuts import render, redirect, get_object_or_404
from .models import Place
from .forms import NewPlaceForm
from .forms import TripReviewForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseForbidden

# Create your views here.

@login_required
def place_list(request):

    """
    if post request, user clicked add. check if valid, then save
    new place to database and redirect to refresh page for get request
    if nota  post or place isn't valid, display page with list and form to add
    """
    if request.method == "POST":
        form = NewPlaceForm(request.POST)
        place = form.save(commit=False) # create new place from form
        place.user = request.user
        if form.is_valid(): # check against db constraints
            place.save() # saves to db
            return redirect('place_list') # redirects to get view

    # if not POST or not valid, just render the page
    # with same form and list
    places = Place.objects.filter(user=request.user).filter(visited=False).order_by('name')
    new_place_form = NewPlaceForm
    return render(request, 'travel_wishlist/wishlist.html', { 'places': places, 'new_place_form': new_place_form })

@login_required
def places_visited(request):
    # Place.objects pulls from the database, filtered to only show visited=True, then that info is rendered on the page
    visited = Place.objects.filter(user=request.user).filter(visited=True)
    return render(request, 'travel_wishlist/visited.html', { 'visited': visited })

@login_required
def place_was_visited(request, place_pk):
    # this updates a database entry using the automatic pk, but if the pk doesn't exist, it'll 404 instead of saving
    if request.method == "POST":
        place = get_object_or_404(Place, pk=place_pk)
        print(place.user, request.user)
        if place.user == request.user: # only auth'd users can select visited
            place.visited = True
            place.save()
        else:
            return HttpResponseForbidden()
    
    return redirect('place_list')

@login_required
def place_details(request, place_pk):
    place = get_object_or_404(Place, pk=place_pk)

    if place.user != request.user:
        return HttpResponseForbidden()

    if request.method == 'POST':
        form = TripReviewForm(request.POST, request.FILES, instance=place)
        # instance is model object to update with data

        if form.is_valid():
            form.save()
            messages.info(request, 'Trip information updated!')
        else:
            messages.error(request, form.errors) # temp, should be improved
        
        return redirect('place_details', place_pk=place_pk)

    else: # GET details
        if place.visited:
            review_form = TripReviewForm(instance=place) # prepopulate with data
            return render(request, 'travel_wishlist/place_detail.html', {'place': place, 'review_form': review_form})
        else:
            return render(request, 'travel_wishlist/place_detail.html', {'place': place} )
 
@login_required
def delete_place(request, place_pk):
    place = get_object_or_404(Place, pk=place_pk)
    if place.user == request.user:
        place.delete()
        return redirect('place_list')
    else:
        return HttpResponseForbidden()
