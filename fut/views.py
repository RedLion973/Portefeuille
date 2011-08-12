# -*- coding: UTF-8 -*- #
from datetime import date, timedelta
from django.views.generic import DetailView, ListView, CreateView
from FUTFactory.fut.models import FUT
from FUTFactory.edm.models import Folder
from FUTFactory.settings import STATIC_URL

class FUTListView(ListView):
    queryset = FUT.objects.order_by('state__phase')
    context_object_name = 'futs_list'
    paginate_by = 10
    template_name = 'futs/index.html'

class FUTDetailView(DetailView):
    model = FUT
    context_object_name = 'fut'
    template_name = 'futs/detail.html'
    
    def get_folders(self, folder_id):
        f = Folder.objects.get(id=folder_id)
        #tree = '<li><span class="folder_links"><a href="{% url \'folder-new\' ' + f.id + ' %}">Ajouter un répertoire</a> | <a href="{% url \'{document-new\' ' + f.id + ' %}">Ajouter un document</a></span><span class="folder">' + f.name + '</span></span>'
        tree = u'<li><span class="folder">' + f.name + ' | Ajouter <a class="folder_links" href="#"><img src="' + STATIC_URL + 'img/folder.png" alt="Add Folder" height="12px" width="12px" /></a> ou <a class="folder_links" href="#"><img src="' + STATIC_URL + 'img/file.png" alt="Add File" height="12px" width="12px" /></span>'
        if not f.documents.all().count() == 0:
            tree += '<ul>'
            for d in f.documents.all():
                tree += '<li><span class="file">' + d.name + '</span></li>'
            tree += '</ul>'
        for folder in f.subfolders.all():
            self.get_folders(self, folder.id)
        tree += '</li>'
        return tree
    
    def get_number_of_days(self, d1, d2):
        days = 0
        weekends = 0
        while d1 + timedelta(days) <= d2:
            d0 = d1 + timedelta(days)
            if d0.weekday() > 4:
                weekends += 1
            days += 1
        return {'number_of_days': days, 'number_of_working_days': days - weekends}
    
    def get_context_data(self, **kwargs):
        context = super(DetailView, self).get_context_data(**kwargs)
        space = self.object.sharing_doc_space
        tree = self.get_folders(space.id)
        context.update({
            'tree': tree
        })
        if self.object.has_prev_planning() == True:
            s = self.get_number_of_days(self.object.scheduled_start_date, self.object.scheduled_end_date)
            context.update({
                'scheduled_days': s['number_of_days'],
                'scheduled_days_nw': s['number_of_working_days']
            })
        if self.object.has_eff_planning() == True:
            e = self.get_number_of_days(self.object.effective_start_date, self.object.effective_end_date)
            context.update({
                'effective_days': e['number_of_days'],
                'effective_days_nw': e['number_of_working_days']
            })
        return context
