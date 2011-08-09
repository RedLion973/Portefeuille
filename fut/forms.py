# -*- coding: UTF-8 -*- #
from django import forms
from FUTFactory.fut.models import FUT, Actor

# FUT ModelForm with custom validation
class FUTModelForm(forms.ModelForm):
    # Champs du formulaire
    release_manager = forms.ModelChoiceField(required=False, queryset=Actor.objects.filter(actor_type__name='Release Manager'))
    leader = forms.ModelChoiceField(required=False, queryset=Actor.objects.filter(actor_type__name='FUTFactory'))
    support = forms.ModelChoiceField(required=False, queryset=Actor.objects.filter(actor_type__name='FUTFactory'))
    
    # Méthodes
    def clean(self):
        cleaned_data = self.cleaned_data
        leader = cleaned_data.get("leader")
        support = cleaned_data.get("support")
        release_manager = cleaned_data.get("release_manager")
        if leader and support and release_manager:
            if leader == support or leader==release_manager or release_manager==support:
                msg = u"Ces champs doivent comporter des valeurs différentes."
                self._errors["leader"] = self.error_class([msg])
                self._errors["support"] = self.error_class([msg])
                self._errors["release_manager"] = self.error_class([msg])
                del cleaned_data["cc_myself"]
                del cleaned_data["subject"]
        return cleaned_data
    
    # Meta
    class Meta:
        model = FUT