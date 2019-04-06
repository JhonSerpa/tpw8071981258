from django.db import models
from django.contrib.auth.models import User as uu

class MediaAuthor(models.Model):
    name = models.CharField(max_length=70)
    surname = models.CharField(max_length=70)
    birthday = models.DateField

    img = models.ImageField(upload_to='gallery', default='gallery/no-img.png')

    def __str__(self):
        return self.name


class Media(models.Model):
    name = models.CharField(max_length=70)
    date_published = models.DateField
    date_added = models.DateTimeField
    author = models.ForeignKey(MediaAuthor, on_delete=models.CASCADE)
    description = models.CharField(max_length=500)
    img = models.ImageField(upload_to='gallery', default='gallery/no-img.png')

    def __str__(self):
        return self.name


class User(models.Model):
    img = models.ImageField(upload_to='gallery', default='gallery/no-img.png')
    authentication = models.ForeignKey(uu, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return "User" + str(self.id)


class Review(models.Model):
    author = models.ForeignKey(uu, on_delete=models.CASCADE)
    media = models.ForeignKey(Media, on_delete=models.CASCADE)
    rate = models.PositiveIntegerField(default=0)
    review = models.CharField(max_length=1000)

    def __str__(self):
        return "%10s|%10s".format(self.author, self.media)
