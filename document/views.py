from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, ListView, DetailView, UpdateView
from .models import Document
from .forms import DocumentModelForm
from django.urls import reverse
from django.db.models import Q


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
        q = self.request.GET.get('q')
        if q:
            return queryset.filter(
                Q(title__icontains=q) |
                Q(text__icontains=q) |
                Q(author__username__icontains=q) |
                Q(source__name__icontains=q))
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
