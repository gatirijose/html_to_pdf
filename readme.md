# Here we are  going to create a blog whereby we can generate our content into ```pdf ``` using ```Xhtml2pdf ``` library #

## 1. run the following command to install required packages for the project: ##

```
pip install pillow xhtml2pdf django django-tinymce  django-bootstrap5 django-bootstrap-datepicker-plus
```
## 2. We will then create our project ##

```
django-admin startproject pdfgenerator .
```

## 3. On the same directory as the ```manage.py``` file we will create an app called ```pdfapp```

```
python manage.py startapp pdfapp
```
## 4. on the `setings.py` file we will add the following

```
INSTALLED_APPS = [
    ...,
    'bootstrap5',
    'bootstrap_datepicker_plus',
    'pdfapp.apps.PdfappConfig',
    'tinymce',
]

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [`BASE_DIR / 'templates' `],
        ...
    },
]

MEDIA_URL = ''
MEDIA_ROOT = BASE_DIR / ''
STATIC_ROOT = BASE_DIR / 'staticfiles'

STATICFILES_DIRS = [
    BASE_DIR / 'static',
]
```

## 5. On the same directory as you` manage.py` file create two folders `templates` and `static`

## 6. In your templates folder create your `base.html` file whereby our templates will inherit properties.

```
<!DOCTYPE html>
{% load static %}
{% load bootstrap5 %}
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="../../cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css"><link rel="stylesheet" href="../../cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.2.3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-rbsA2VBKQhggwzxH7pPCaAqO46MgnOM80zW1RWuH61DGLwZJEdK2Kadq2F9CUG65" crossorigin="anonymous">
   {{form.media}}
   <title>{% block title %}{% endblock %}</title>
</head>
<body>
   <nav class="navbar navbar-expand-lg navbar-fixed-top navbar-dark" style="background-color: rgb(44, 44, 66);">
      <div class="container">
        <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarTogglerDemo01" aria-controls="navbarTogglerDemo01" aria-expanded="false" aria-label="Toggle navigation">
          <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarTogglerDemo01">
          <a class="navbar-brand" href="{% url 'home' %}">PdfCreator</a>
          <ul class="navbar-nav me-auto mb-2 mb-lg-0">
            <li class="nav-item">
              <a class="nav-link active" aria-current="page" href={% url 'new' %}>Home</a>
            </li>
          </ul>
          <form class="d-flex" role="search"> 
            {% block navbar_link %} {% endblock %}    
          </form>
        </div>
      </div>
    </nav>
<br>

   <br>
   <div class="container">
        {% block content %}
            
        {% endblock %}
        
    </div>
   <script src="https://cdn.jsdelivr.net/npm/@popperjs/core@2.11.6/dist/umd/popper.min.js" integrity="sha384-oBqDVmMz9ATKxIep9tiCxS/Z9fNfEXiDAYTujMAeBAsjFuCZSmKbSSUnQlmh/jp3" crossorigin="anonymous"></script>
<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.2.3/dist/js/bootstrap.min.js" integrity="sha384-cuYeSxntonz0PPNlHhBs68uyIAVpIIOZZ5JqeqvYYIcEL727kskC66kF92t6Xl2V" crossorigin="anonymous"></script>
</body>
</html>
```

## 7. Open the `models.py` file on the `pdfapp` folder and create the following model:

```
from django.db import models
from tinymce.models import HTMLField
from django.urls import reverse



class Post(models.Model):
    title = models.CharField(max_length=200)
    content = HTMLField()
    date_created = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):

        return reverse('details', kwargs={'pk': self.pk})
```

## 8. Open the `admin.py` file to register the model `Post`.

```
from django.contrib import admin

from .models import Post



@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'date_created']
    list_filter = ['date_created']
```

## 9.Open the `views.py` on the same directory and create the views as shown below.

```
from .models import Post
from django.views.generic import *
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.template.loader import get_template
from xhtml2pdf import pisa

class PostCreateView(CreateView):
    model = Post
    fields = '__all__'



class PostListView(ListView):
    model = Post


class PostDetailView(DetailView):
    model = Post


def render_pdf_view(request, *args, **kwargs):
    pk = kwargs.get('pk')
    post = get_object_or_404(Post, pk=pk)
    template_path = 'pdfapp\pdf.html'
    context = {'post': post}
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'filename="render_pdf_{post.title}.pdf"'
    template = get_template(template_path)
    html = template.render(context)
    pisa_status = pisa.CreatePDF(
        html, dest=response)
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response
```

## 10. create `templates\pdfapp` folder on the pdfapp directory.

## 11. in the pdfapp\templates directory we will create four files namely `pdf.html`, `post_form.html`, `post_list.html` and `post_detail.html` which are as shown below:
##

# a. post_list.html

```
{% extends 'base.html' %}
{% load bootstrap5 %}
{% block title %}Home{% endblock %}

{% block content %}
    <div class="row">
        {% for object in object_list %}
            <div class="col-md-4">
                <h3>{{object.title}}</h3>
                <p class="text-muted text-right"><small>{{object.date_created}}</small></p>
                <p>{{object.content|striptags|truncatewords_html:1 }} <a href="{% url 'details' pk=object.pk %}">read more</a></p>
            </div>
        {% endfor %}
    </div>
{% endblock %}
```

# b. post_detail.html
```
{% extends 'base.html' %}
{% load bootstrap5 %}
{% block title %}{{object.title|truncatewords:1}}{% endblock %}
{% block navbar_link %}<a class="text-danger" href="{% url 'pdf' pk=object.pk %}"><i style="width: 1.5em; height: 1.5rem;" class="fas fas fa-file-pdf" type="submit"></i></a>
{% endblock %}
{% block content %}

    <h1 style="text-decoration: underline;" class="text-center page-title">{{object.title}}</h1>
    <hr>
    <p class="text-muted text-right"><small>{{object.date_created}}</small></p>
    {{object.content|safe}}
{% endblock %}
```

# c. post_form.html
```
{% extends 'base.html' %}
{% load bootstrap5 %}
{% block title %}{{object.title|truncatewords:1}}{% endblock %}
{{form.media}}
{% block content %}
    <form  method="POST">
        {% csrf_token %}
        {% bootstrap_form form %}
        <br>
        {% bootstrap_button "Save" button_type="submit" button_class="btn btn-primary" %}
    </form>
{% endblock %}
```
# d. pdf.html
```
<!DOCTYPE html>
<html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            
            h1{
                font-size: 3em;
                text-align: center;
                color: red;
            }
            h6{
                font-size: 1.7em;
                text-align: center;
            }
            h5{
                font-size: 1.9em;
                text-align: center;
            }
            h4{
                font-size: 2.1em;
                text-align: center;
            }
            h3{
                font-size: 2.4em;
                text-align: center;
            }
            h2{
                font-size: 2.7em;
                text-align: center;
            }
            p{
                font-size: 1.5em;
                text-align: start;
            }
            text{
                text-align: start; 
                color: red;
            }
        </style>
        <title>{{post.title}}</title> 
    </head>
    <body>
        <h1 class="text-center">{{post.title}}</h1> 
        <small style="display: inline; float: right; text-align: start;">{{post.date_created}}</small>
        <hr>
        {{post.content|safe}}
    </body>
</html>
```

## 12. On your terminal or command prompt `cd ` to the same directory as your `manage.py` file and run `python manage.py makemigration` and then `python manage.py migrate`

## 13. Run `python manage.py runserver` and you can start editing the content 

## 14. in the details page at the right hand side of the navbar you can click the pdf icon to see the pdf file.
