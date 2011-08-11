import datetime
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
        sd = 0
        ed = 0
        sd_no_weekend = 0
        ed_no_weekend = 0
        if self.object.has_planning:
            s_daydiff = self.object.scheduled_end_date.weekday() - self.object.scheduled_start_date.weekday()
            sd_no_weekend = ((self.object.scheduled_end_date - self.object.scheduled_start_date).days - s_daydiff) / 7 * 5 + min(s_daydiff, 5)
            e_daydiff = self.object.effective_end_date.weekday() - self.object.effective_start_date.weekday()
            ed_no_weekend = ((self.object.effective_end_date - self.object.effective_start_date).days - e_daydiff) / 7 * 5 + min(e_daydiff, 5)
            ed = (self.object.effective_end_date - self.object.effective_start_date).days
            sd = (self.object.scheduled_end_date - self.object.scheduled_start_date).days
        context.update({
            'tree': tree,
            'scheduled_days': sd,
            'effective_days': ed,
            'scheduled_days_nw': sd_no_weekend,
            'effective_days_nw': ed_no_weekend
        })
        return context