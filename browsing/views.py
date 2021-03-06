from django_tables2 import SingleTableView, RequestConfig
from documents.models import Document, ArchObject, DigObject
from .filters import DocumentListFilter, ArchObjectListFilter, DigObjectListFilter
from .tables import DocumentTable, ArchObjectTable, DigObjectTable
from .forms import GenericFilterFormHelper


class GenericListView(SingleTableView):
    filter_class = None
    formhelper_class = None
    context_filter_name = 'filter'
    paginate_by = 25

    def get_queryset(self, **kwargs):
        qs = super(GenericListView, self).get_queryset()
        self.filter = self.filter_class(self.request.GET, queryset=qs)
        self.filter.form.helper = self.formhelper_class()
        return self.filter.qs

    def get_table(self, **kwargs):
        table = super(GenericListView, self).get_table()
        RequestConfig(self.request, paginate={
            'page': 1, 'per_page': self.paginate_by}).configure(table)
        return table

    def get_context_data(self, **kwargs):
        context = super(GenericListView, self).get_context_data()
        context[self.context_filter_name] = self.filter
        return context


class DocumentListView(GenericListView):
    model = Document
    table_class = DocumentTable
    template_name = 'browsing/document_list_generic.html'
    filter_class = DocumentListFilter
    formhelper_class = GenericFilterFormHelper


class ArchObjectListView(GenericListView):
    model = ArchObject
    table_class = ArchObjectTable
    template_name = 'browsing/archobject_list_generic.html'
    filter_class = ArchObjectListFilter
    formhelper_class = GenericFilterFormHelper


class DigObjectListView(GenericListView):
    model = DigObject
    table_class = DigObjectTable
    template_name = 'browsing/digobject_list_generic.html'
    filter_class = DigObjectListFilter
    formhelper_class = GenericFilterFormHelper
