from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, logout
from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse
from django.db import transaction
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Wallpaper, Favourite_wp
from .forms import WallpaperForm, CustomUserForm, CategoryForm
from .models import Category, DownloadHistory
from django.views import View
from django.contrib.auth.decorators import user_passes_test


class RegisterView(View):
    template_name = 'register.html'

    def get(self, request):
        form = CustomUserForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = CustomUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
        return render(request, self.template_name, {'form': form})



def login_view(request):
    error_message = None

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Check if the user is an admin
        admin_user = authenticate(request, username=username, password=password)

        if admin_user and admin_user.is_superuser:
            auth_login(request, admin_user)
            return redirect('inde')

        # Check if the user is a regular user
        user = authenticate(request, username=username, password=password)

        if user is not None:
            auth_login(request, user)
            return redirect('index')
        else:
            error_message ="Invalid Username or password"

    return render(request, 'login.html', {'form': CustomUserForm(),'error_message': error_message})


def index(request):
    wallpapers = Wallpaper.objects.filter(status=0)
    categories = Category.objects.all()
    query = request.GET.get('q', '')
    wallpapers = Wallpaper.objects.filter(Q(title__icontains=query, status=0) | Q(categories__name__icontains=query)).distinct()
    return render(request, 'index.html', {'wallpapers': wallpapers, 'categories': categories, 'query': query})


def inde(request):
    wallpapers = Wallpaper.objects.filter(status=0)
    categories = Category.objects.all()
    query = request.GET.get('q', '')
    wallpapers = Wallpaper.objects.filter(Q(title__icontains=query, status=0) | Q(categories__name__icontains=query)).distinct()
    return render(request, 'admin.html', {'wallpapers': wallpapers, 'categories': categories, 'query': query})


def wallpaper_list(request):
    wallpapers = Wallpaper.objects.all()
    return render(request, 'wallpaper_list.html', {'wallpapers': wallpapers})


def add_wallpaper(request):
    if request.method == 'POST':
        form = WallpaperForm(request.POST, request.FILES)
        if form.is_valid():
            title = form.cleaned_data['title']
            w_image = form.cleaned_data['w_image']

            # Check if a wallpaper with the same title and image already exists
            if Wallpaper.objects.filter(Q(title=title) | Q(w_image=w_image)).exists():
                messages.error(request, 'A wallpaper with the same title or image already exists.')
                return render(request, 'add_wallpaper.html', {'form': form})

            wallpaper = form.save(commit=False)
            wallpaper.uploaded_by = request.user
            wallpaper.save()
            form.save_m2m()
            messages.success(request, 'Wallpaper added successfully.')
            return redirect('index')
    else:
        form = WallpaperForm()

    return render(request, 'add_wallpaper.html', {'form': form})

def custom_admin(request):
    wallpapers = Wallpaper.objects.all()
    return render(request, 'admin_view.html', {'wallpapers': wallpapers})


def category_wallpapers(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    wallpapers = category.wallpaper_set.filter(status=0)
    return render(request, 'category_wallpapers.html', {'category': category, 'wallpapers': wallpapers})


def is_admin(user):
    return user.is_superuser


def edit_wallpaper(request, wallpaper_id):
    wallpaper = get_object_or_404(Wallpaper, pk=wallpaper_id)

    # Check if the current user is either the uploader or an admin
    if request.user != wallpaper.uploaded_by and not is_admin(request.user):
        messages.error(request, "You don't have permission to edit this wallpaper.")
        return redirect('index')

    if request.method == 'POST':
        form = WallpaperForm(request.POST, request.FILES, instance=wallpaper)
        if form.is_valid():
            form.save()
            messages.success(request, "Wallpaper updated successfully.")
            return redirect('inde')
    else:
        form = WallpaperForm(instance=wallpaper)

    return render(request, 'edit_wallpaper.html', {'form': form, 'wallpaper': wallpaper})

@user_passes_test(lambda u: u.is_superuser, login_url='index')
def delete_wallpaper(request, wallpaper_id):
    wallpaper = get_object_or_404(Wallpaper, pk=wallpaper_id)

    with transaction.atomic():
        wallpaper.favourites.all().delete()
        wallpaper.delete()

    messages.success(request, "Wallpaper deleted successfully")
    return redirect('index')

@login_required
def download_history(request):
    download_history = DownloadHistory.objects.filter(user=request.user).order_by('-download_time')
    return render(request, 'download_history.html', {'download_history': download_history})

def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin_view')  # Redirect to admin view after adding a category
    else:
        form = CategoryForm()

    return render(request, 'add_category.html', {'form': form})



def ulogout(request):
    logout(request)
    return redirect('index')


@login_required
def add_to_favorites(request, wallpaper_id):
    wallpaper = get_object_or_404(Wallpaper, id=wallpaper_id)

    if Favourite_wp.objects.filter(user=request.user, wallpaper=wallpaper).exists():
        favorite_entry = Favourite_wp.objects.get(user=request.user, wallpaper=wallpaper)
        favorite_entry.delete()
        added = False
    else:
        Favourite_wp.objects.create(user=request.user, wallpaper=wallpaper)
        added = True

    count = Favourite_wp.objects.filter(wallpaper=wallpaper).count()

    # Redirect to the favorites page
    return HttpResponseRedirect(reverse('favorites'))


def remove_from_favorites(request, wallpaper_id):
    wallpaper = get_object_or_404(Wallpaper, id=wallpaper_id)

    # Check if the user is authenticated and if the wallpaper is in their favorites
    if request.user.is_authenticated:
        try:
            favorite_entry = Favourite_wp.objects.get(user=request.user, wallpaper=wallpaper)
            favorite_entry.delete()
        except Favourite_wp.DoesNotExist:
            # Handle case where the favorite entry does not exist
            pass

        # Optionally, you can perform additional actions here

        # Redirect to the favorites page after removal
        return redirect('favorites')
    else:
        # Handle cases where the user is not authenticated
        # You can customize this based on your requirements
        return render(request, 'error_page.html', {'message': 'Unauthorized'})

def favorites_view(request):
    if request.user.is_authenticated:
        favorite_wallpapers = Wallpaper.objects.filter(favourites__user=request.user)
        return render(request, 'favorites.html', {'favorite_wallpapers': favorite_wallpapers})
    else:
        return render(request, 'favorites.html')



from django.http import HttpResponse
from django.template.defaultfilters import slugify

def download_wallpaper(request, wallpaper_id):
    wallpaper = get_object_or_404(Wallpaper, id=wallpaper_id)

    # Set Content-Disposition header to prompt download with the correct filename
    response = HttpResponse(content_type='image/jpeg')
    response['Content-Disposition'] = f'attachment; filename="{slugify(wallpaper.title)}.jpg"'

    # Write the image data to the response
    response.write(wallpaper.w_image.read())

    # Create a DownloadHistory entry
    DownloadHistory.objects.create(user=request.user, wallpaper=wallpaper)

    return response



class WallpaperDetailView(View):
    template_name = 'wallpaper_detail.html'

    def get(self, request, *args, **kwargs):
        wallpaper_id = kwargs['wallpaper_id']
        wallpaper = get_object_or_404(Wallpaper, id=wallpaper_id)
        return render(request, self.template_name, {'wallpaper': wallpaper})
    
from .models import User
class YourwallpaperView(View):
    template_name = 'your_wallpapers.html'

    def get(self, request, user_id):
        user = get_object_or_404(User, id=user_id)
        wallpapers = Wallpaper.objects.filter(uploaded_by=user)
        return render(request, self.template_name, {'user': user, 'wallpapers': wallpapers})


