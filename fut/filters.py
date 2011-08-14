from FUTFactory.lib import django_filters
from FUTFactory.fut.models import FUT

class FUTFilterSet(django_filters.FilterSet):
#    def __init__(self, *args, **kwargs):
#        super(FUTFilterSet, self).__init__(*args, **kwargs)
#        for i in range(0, len(self.filters)):
#            self.filters[i].extra.update({'empty_label': u'Tous'})
            
    class Meta:
        model = FUT
        fields = [
            'name',
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