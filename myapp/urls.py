# wallpapers/urls.py
from django.urls import path
from .views import (
    login_view,
    RegisterView,
    index,
    wallpaper_list,
    add_wallpaper,
    edit_wallpaper,
    delete_wallpaper,
    custom_admin,
    category_wallpapers,
    ulogout,
    add_to_favorites,
    favorites_view,
    inde,
    download_wallpaper,
    WallpaperDetailView,
    YourwallpaperView,
    remove_from_favorites,
    add_category,
    download_history
)

urlpatterns = [
    path('', index, name='index'),
    path('admi/', inde, name='inde'),

    path('login/', login_view, name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('wallpapers/', wallpaper_list, name='wallpaper_list'),
    path('add_wallpaper/', add_wallpaper, name='add_wallpaper'),
    path('edit_wallpaper/<int:wallpaper_id>/', edit_wallpaper, name='edit_wallpaper'),
    path('delete_wallpaper/<int:wallpaper_id>/', delete_wallpaper, name='delete_wallpaper'),
    path('admin_view/', custom_admin, name='admin_view'),
    path('category_wallpapers/<int:category_id>/', category_wallpapers, name='category_wallpapers'),
    path('ulogout/', ulogout, name='ulogout'),
    path('add_to_favorites/<int:wallpaper_id>/', add_to_favorites, name='add_to_favorites'),
    path('favorites/', favorites_view, name='favorites'),
    path('download/<int:wallpaper_id>/', download_wallpaper, name='download_wallpaper'),
    path('wallpaper/<int:wallpaper_id>/', WallpaperDetailView.as_view(), name='wallpaper_detail'),
    path('your_wallpapers/<int:user_id>/', YourwallpaperView.as_view(), name='your_wallpapers'),
    path('remove_from_favorites/<int:wallpaper_id>/', remove_from_favorites, name='remove_from_favorites'),
    path('add_category/', add_category, name='add_category'),
    path('download_history/', download_history, name='download_history'),



]
