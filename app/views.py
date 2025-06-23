# capa de vista/presentación

from django.shortcuts import redirect, render
from .layers.services import services
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from .layers.services.services import getAllImages
from .layers.services.services import getAllFavourites
from app.config import config 
from .layers.services.services import filterByType
from .layers.services.services import getAllFavourites

def index_page(request):
    return render(request, 'index.html')

def getAllImageAndFavoriteList(request):
    images = services.getAllImages()
    return images

# esta función obtiene 2 listados: uno de las imágenes de la API y otro de favoritos, ambos en formato Card, y los dibuja en el template 'home.html'.
def home(request):
    images = getAllImageAndFavoriteList(request)
    try:
        favourite_list = getAllFavourites(request)
    except (ImportError, AttributeError):
        favourite_list = []
    return render(request, 'home.html', { 'images': images, 'favourite_list': favourite_list })

def search(request):
    if request.method == 'POST':
        name = request.POST.get('query', '').lower().strip()

        if name:
            all_cards = getAllImages()
            images = [card for card in all_cards if name in card.name.lower()]
            favourite_list = []

            return render(request, 'home.html', { 
                'images': images, 
                'favourite_list': favourite_list 
            })

    return redirect('home')

# función utilizada para filtrar por el tipo del Pokemon
def filter_by_type(request):
    type = request.POST.get('type', '')

    if type != '':
        favourite_list = []
        images = filterByType(type) if type else []

        return render(request, 'home.html', { 'images': images, 'favourite_list': favourite_list })
    else:
        return redirect('home')

# Estas funciones se usan cuando el usuario está logueado en la aplicación.
@login_required
def getAllFavouritesByUser(request):
    favourite_list= services.getAllFavourites(request)
    return render(request, 'favourites.html', { 'favourite_list': favourite_list })

@login_required
def saveFavourite(request):
    services.saveFavourite(request)
    return redirect('home')

@login_required
def deleteFavourite(request):
    services.deleteFavourite(request)
    return redirect('home')

@login_required
def exit(request):
    logout(request)
    return redirect('home')