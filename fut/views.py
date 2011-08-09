from django.views.generic import DetailView, ListView
from FUTFactory.fut.models import FUT
from FUTFactory.edm.models import Folder



class FUTListView(ListView):
    queryset = FUT.objects.order_by('state__phase')
    context_object_name = 'futs_list'
    paginate_by = 10
    template_name = 'futs/index.html'

class FUTDetailView(DetailView):
    model = FUT
    context_object_name = 'fut'
    template_name='futs/detail.html'
    
    def get_folders(self, folder_id):
        f = Folder.objects.get(id=folder_id)
        tree = '<li><span class="folder">' + f.name + '</span>'
        if not f.documents.all().count() == 0:
            tree += '<ul>'
            for d in f.documents.all():
                tree += '<li><span class="file">' + d.name + '</span></li>'
            tree += '</ul>'
        for folder in f.subfolders.all():
            self.get_folders(self, folder.id)
        tree += '</li>'
        return tree
    
    def get_context_data(self, **kwargs):
        context = super(DetailView, self).get_context_data(**kwargs)
        space = self.object.sharing_doc_space
        tree = self.get_folders(space.id)
        context.update({
            'tree': tree
        })
        return context