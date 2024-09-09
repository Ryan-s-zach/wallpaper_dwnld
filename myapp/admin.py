from django.contrib import admin
from .models import Category, Wallpaper,Favourite_wp,DownloadHistory



class WallpaperAdmin(admin.ModelAdmin):
    list_display = ('title', 'resolution_width', 'resolution_height', 'file_size', 'uploaded_by', 'uploaded_at')
    search_fields = ('title', 'uploaded_by__username')

admin.site.register(Wallpaper, WallpaperAdmin)
admin.site.register(Category)
admin.site.register(Favourite_wp)
admin.site.register(DownloadHistory)

