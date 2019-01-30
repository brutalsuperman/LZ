from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, ListView, DetailView, UpdateView
from .models import Document
from .forms import DocumentModelForm
from django.urls import reverse
# from django.db.models import Q
from datetime import datetime
from django.http import JsonResponse
from .tasks import download_selected_documents_task


class DocumentCreateView(LoginRequiredMixin, CreateView):
    model = Document
    # fields = ['title', 'text', 'url', 'source']
    form_class = DocumentModelForm

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.author = self.request.user
        return super(DocumentCreateView, self).form_valid(form)


class DocumentListView(ListView):
    model = Document

    def get_queryset(self):
        queryset = super(DocumentListView, self).get_queryset()
        text = self.request.GET.get('text')
        title = self.request.GET.get('title')
        author = self.request.GET.get('author')
        source = self.request.GET.get('source')
        create = self.request.GET.get('created')
        update = self.request.GET.get('update')
        print(self.request.GET.getlist('checks'))
        if text:
            queryset = queryset.filter(text__icontains=text)
        if title:
            queryset = queryset.filter(title__icontains=title)
        if author:
            queryset = queryset.filter(author__username__icontains=author)
        if source:
            queryset = queryset.filter(source__name__icontains=source)
        if create:
            created = datetime.strptime(create, '%Y-%m-%d')
            queryset = queryset.filter(created__date=created)
        if update:
            updated = datetime.strptime(update, '%Y-%m-%d')
            queryset = queryset.filter(update__date=updated)
        return queryset


class DocumentDetailView(DetailView):
    model = Document


class DocumentUpdateView(UpdateView):
    model = Document
    # fields = ['title', 'text', 'url', 'source']
    form_class = DocumentModelForm

    def form_valid(self, form):
        document = Document.objects.get(pk=self.object.pk)
        if document.editable() or self.request.user.is_superuser:
            return super(DocumentUpdateView, self).form_valid(form)
        else:
            msg = 'You can edit just first hour after create'
            form.add_error(None, msg)
            return super(DocumentUpdateView, self).form_invalid(form)

    def get_success_url(self):
        return reverse('document:detail', kwargs={'pk': self.object.pk})


def json_docs(request):
    if request.GET:
        documents = Document.objects.filter(id__in=request.GET.getlist('checks')).values()
        data = list(documents)
        if request.GET.get('to_file'):
            download_selected_documents_task.delay(data)
        return JsonResponse(data, safe=False)

