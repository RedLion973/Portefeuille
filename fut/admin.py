# -*- coding: UTF-8 -*- #
from django.contrib import admin
from FUTFactory.fut.models import FUT, Phase, Step, Role, Type, TargetCustomersType, Domain, Actor, ActorType
from FUTFactory.fut.forms import FUTModelForm
    
class FUTAdmin(admin.ModelAdmin):
    form = FUTModelForm
    readonly_fields = ('sharing_doc_space',)
    fieldsets = [
        (None, {'fields': ['name','description'], 'classes': ['wide', 'extrapretty']}),
        ('Planning', {'fields': ['scheduled_start_date', 'scheduled_end_date', 'effective_start_date', 'effective_end_date', 'state']}),
        ('Détails', {'fields': ['target_customers', 'expected_number_of_futers', 'effective_number_of_futers', 'fut_type', 'domain']}),
        ('Staff', {'fields': ['release_manager', 'leader', 'support', 'role_ff']}),
        (None, {'fields': ['comments','sharing_doc_space'], 'classes': ['wide']}),       
    ]
    list_display = [
                    'name', 'description', 'state', 'fut_type', 'domain',
                    'release_manager', 'leader', 'support', 'role_ff',
    ]
    list_filter = ['leader','support','domain', 'role_ff', 'release_manager','fut_type',]
    search_fields = ['name', 'description',]

class StepAdmin(admin.ModelAdmin):
    list_display = ['phase', 'name']
    
class PhaseAdmin(admin.ModelAdmin):
    list_display = ['name', 'rank', 'processing']
    ordering = ['rank', 'processing']

class ActorAdmin(admin.ModelAdmin):
    list_display = ['actor_type', 'get_full_name']

admin.site.register(FUT, FUTAdmin)
admin.site.register(Phase, PhaseAdmin)
admin.site.register(Step, StepAdmin)
admin.site.register(Role)
admin.site.register(Type)
admin.site.register(Domain)
admin.site.register(TargetCustomersType)
admin.site.register(ActorType)
admin.site.register(Actor, ActorAdmin)