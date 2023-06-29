from django.db import models
from tinymce.models import HTMLField
from django.urls import reverse

# Create your models here.


class Post(models.Model):
    title = models.CharField(max_length=200)
    content = HTMLField()
    date_created = models.DateField(auto_now_add=True)

    def get_absolute_url(self):

        return reverse('details', kwargs={'pk': self.pk})
