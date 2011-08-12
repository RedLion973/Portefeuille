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
	ssd = cleaned_data.get("scheduled_start_date")
	sed = cleaned_data.get("scheduled_end_date")
	esd = cleaned_data.get("effective_start_date")
	eed = cleaned_data.get("effective_end_date")
        if leader and support:
            if leader == support:
                msg = u"Ces champs doivent comporter des valeurs différentes."
                self._errors["leader"] = self.error_class([msg])
                self._errors["support"] = self.error_class([msg])
                del cleaned_data["leader"]
                del cleaned_data["support"]
	if ssd and sed:
	    if sed < ssd:
		msg = u"La date prévue de fin est antérieure à celle de début."
                self._errors["scheduled_start_date"] = self.error_class([msg])
                self._errors["scheduled_end_date"] = self.error_class([msg])
                del cleaned_data["scheduled_start_date"]
                del cleaned_data["scheduled_end_date"]
	if esd and eed:
            if eed < esd:
                msg = u"La date effective de fin est antérieure à celle de début."
                self._errors["effective_start_date"] = self.error_class([msg])
                self._errors["effective_end_date"] = self.error_class([msg])
                del cleaned_data["effective_start_date"]
                del cleaned_data["effective_end_date"]
        return cleaned_data
    
    # Meta
    class Meta:
        model = FUT
