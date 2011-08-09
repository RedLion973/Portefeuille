from django.views.generic import DetailView, ListView
from FUTFactory.fut.models import FUT
from FUTFactory.edm.models import Folder
from FUTFactory.edm.views import get_folders

class FUTListView(ListView):
    queryset = FUT.objects.order_by('state__phase')
    context_object_name = 'futs_list'
    paginate_by = 10
    template_name = 'futs/index.html'

class FUTDetailView(DetailView):
    model = FUT
    context_object_name = 'fut'
    template_name='futs/detail.html'
    
    def get_context_data(self, **kwargs):
        context = super(DetailView, self).get_context_data(**kwargs)
        space = self.object.sharing_doc_space
        tree = get_folders(space.id)
        context.update({
            'tree': tree
        })
        return context