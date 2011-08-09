from django.views.generic import TemplateView
from FUTFactory.fut.models import FUT

class HomeView(TemplateView):
    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        context.update({
            'futs_list': FUT.objects.filter(state__phase__name='En cours')[:10]
        })
        return context