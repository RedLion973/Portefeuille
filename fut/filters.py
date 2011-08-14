from FUTFactory.lib import django_filters
from FUTFactory.fut.models import FUT

class FUTFilterSet(django_filters.FilterSet):            
    class Meta:
        model = FUT
        fields = [
            'state', 
            'scheduled_start_date', 
            'scheduled_end_date', 
            'effective_start_date', 
            'effective_end_date',
            'domain',             
            'fut_type',
            'release_manager',
            'leader',
            'support'
        ]
#    
#    def __init__(self, *args, **kwargs):
#        super(FUTFilterSet, self).__init__(*args, **kwargs)
#        self.filters['state'].extra.update({'empty_label': u'Tous'})
#        self.filters['scheduled_start_date'].extra.update({'empty_label': u'Tous'})
#        self.filters['scheduled_end_date'].extra.update({'empty_label': u'Tous'})
#        self.filters['effective_start_date'].extra.update({'empty_label': u'Tous'})
#        self.filters['effective_end_date'].extra.update({'empty_label': u'Tous'})
#        self.filters['domain'].extra.update({'empty_label': u'Tous'})
#        self.filters['fut_type'].extra.update({'empty_label': u'Tous'})
#        self.filters['release_manager'].extra.update({'empty_label': u'Tous'})
#        self.filters['leader'].extra.update({'empty_label': u'Tous'})
#        self.filters['support'].extra.update({'empty_label': u'Tous'})