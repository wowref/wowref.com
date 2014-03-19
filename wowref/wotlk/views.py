from django.views.generic import DetailView

from .items import Item


class ItemDetailView(DetailView):
    context_object_name = 'item'
    template_name = 'item-detail.html'

    def get_object(self):
        return Item(self.kwargs['pk'])
