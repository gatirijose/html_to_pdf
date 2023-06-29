from django.urls import path
from .views import *
urlpatterns = [
    path('', PostListView.as_view(), name='home'),
    path('<int:pk>/', PostDetailView.as_view(), name='details'),
    path('pdf/<int:pk>', render_pdf_view, name="pdf"),
    path('new/', PostCreateView.as_view(), name='new'),
]
