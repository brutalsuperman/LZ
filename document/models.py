from django.db import models
from account.models import Profile
import datetime
from django.urls import reverse
# Create your models here.


class Source(models.Model):
    sid = models.CharField(max_length=100)
    name = models.CharField(max_length=200)
    url = models.URLField()

    def __str__(self):
        return self.name


class Document(models.Model):
    title = models.CharField(unique=True, max_length=100)
    text = models.TextField(unique=True)
    url = models.URLField()
    created = models.DateTimeField(auto_now_add=True)
    source = models.ForeignKey(Source, on_delete=models.SET_NULL, null=True)
    updated = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True)
    edited_times = models.IntegerField(default=0)

    def __str__(self):
        return self.title

    def editable(self):
        if (self.created + datetime.timedelta(hours=1)) < datetime.datetime.now(datetime.timezone.utc):
            return False
        else:
            return True

    def get_absolute_url(self):
        return reverse('document:detail', kwargs={'pk': self.pk})

    def save(self, *args, **kwargs):
        if not self.pk:
            super().save(*args, **kwargs)
        else:
            self.edited_times += 1
            super().save(*args, **kwargs)
