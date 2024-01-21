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
    template_path = 'templates\pdfapp\pdf.html'
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
