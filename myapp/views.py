from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
import os


import datetime

def log_access(view_func):
    def wrapper(request, *args, **kwargs):
        print(f"[{datetime.datetime.now()}] View accessed: {view_func.__name__}")
        return view_func(request, *args, **kwargs)
    return wrapper

from .forms import ContactForm, SubscriberForm, FavoriteGameForm
from .models import Contact, Subscriber, FavoriteGame  # Ensure all models are imported

# Home page
@log_access
def home(request):
    return render(request, 'myapp/home.html', {'name': 'Yashvardhan Rai'})

# About page
def about(request):
    return render(request, 'myapp/about.html')

# Services page
def services(request):
    return render(request, 'myapp/services.html')

# Contact Us page (Create)
@log_access
def contacts(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('contact_thankyou')
    else:
        form = ContactForm()
    return render(request, 'myapp/contacts.html', {'form': form})

# Contact Thank You page
def contact_thankyou(request):
    return render(request, 'myapp/contact_thankyou.html')

# Static file reader
def static_file(request):
    file_path = os.path.join(settings.BASE_DIR, 'myapp/static/info.txt')
    try:
        with open(file_path, 'r') as file:
            content = file.read()
        return HttpResponse(content, content_type='text/plain')
    except FileNotFoundError:
        return HttpResponse("The file 'info.txt' was not found.", status=404)

# Newsletter subscribe and view
def newsletter_subscribe(request):
    success = False
    form = SubscriberForm()
    subscribers = None

    if request.method == 'POST':
        form = SubscriberForm(request.POST)
        if form.is_valid():
            form.save()
            success = True
    elif request.method == 'GET' and request.GET.get('show') == 'subscribers':
        subscribers = Subscriber.objects.all()

    return render(request, 'myapp/newsletter.html', {
        'form': form,
        'success': success,
        'subscribers': subscribers
    })

# Favorite Games List (Read)
def favorite_games_list(request):
    games = FavoriteGame.objects.all()
    return render(request, 'myapp/favorite_games_list.html', {'games': games})

# Create Favorite Game
def favorite_game_create(request):
    if request.method == 'POST':
        form = FavoriteGameForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('favorite_games_list')
        else:
            return render(request, 'myapp/favorite_game_form.html', {'form': form, 'error': 'Form is invalid. Please correct the errors below.'})
    else:
        form = FavoriteGameForm()
    return render(request, 'myapp/favorite_game_form.html', {'form': form})

# Update Favorite Game
def favorite_game_update(request, pk):
    game = get_object_or_404(FavoriteGame, pk=pk)
    if request.method == 'POST':
        form = FavoriteGameForm(request.POST, instance=game)
        if form.is_valid():
            form.save()
            return redirect('favorite_games_list')
        else:
            return render(request, 'myapp/favorite_game_form.html', {'form': form, 'error': 'Form is invalid. Please correct the errors below.'})
    else:
        form = FavoriteGameForm(instance=game)
    return render(request, 'myapp/favorite_game_form.html', {'form': form})

# Delete Favorite Game
def favorite_game_delete(request, pk):
    game = get_object_or_404(FavoriteGame, pk=pk)
    if request.method == 'POST':
        game.delete()
        return redirect('favorite_games_list')
    return render(request, 'myapp/favorite_game_confirm_delete.html', {'game': game})
