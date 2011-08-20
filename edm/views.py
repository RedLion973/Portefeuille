from django.views.generic import CreateView
from FUTFactory.fut.models import FUT
from FUTFactory.edm.models import Folder

class FolderCreate(CreateView):
    model = Folder
    template_name = 'folders/new.html'

    def get_context_data(self, **kwargs):
        context = super(CreateView, self).get_context_data(**kwargs)
        space = Folder.self.object.sharing_doc_space
        tree = self.get_folders(space.id)
        context.update({
            'tree': tree
        })
        return context
