from django.db import models
from django.contrib.auth.models import User
# from .models import Wallpaper

class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Wallpaper(models.Model):
    title = models.CharField(max_length=255)
    w_image = models.ImageField(upload_to='wallpapers/')
    resolution_width = models.IntegerField()
    resolution_height = models.IntegerField()
    file_size = models.DecimalField(max_digits=5, decimal_places=2)
    status = models.BooleanField(default=False, help_text="0-show, 1-hidden")
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    categories = models.ManyToManyField(Category)  # Many-to-Many relationship
    
    def __str__(self):
        return self.title
    
class Favourite_wp(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    wallpaper = models.ForeignKey(Wallpaper, related_name='favourites', on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.wallpaper.title}"
    

class DownloadHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    wallpaper = models.ForeignKey(Wallpaper, on_delete=models.CASCADE)
    download_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.wallpaper.title} - {self.download_time}"
