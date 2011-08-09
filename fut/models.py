# -*- coding: UTF-8 -*- #
from django.db import models
from django.utils.encoding import smart_unicode
from FUTFactory.edm.models import Folder

# Phase du processus
class Phase(models.Model):
    # Attributs
    name = models.CharField(u'Nom', max_length=650, unique=True)
    description = models.TextField(u'Description', blank=True)
    
    # Méthodes
    def __unicode__(self):
        return u'%s' % (self.name)
    
    # Meta
    class Meta:
        verbose_name, verbose_name_plural = (u'Phase du process', u'Phases du process')

# Etape d'une phase du processus
class Step(models.Model):
    # Attributs
    phase = models.ForeignKey(Phase, verbose_name=u'Phase du process')
    name = models.CharField(u'Nom', max_length=650, unique=True)
    description = models.TextField(u'Description', blank=True)
    conclusion = models.BooleanField(default=0)
    
    # Méthodes
    def __unicode__(self):
        return u'%s' % (self.name)
    
    # Meta
    class Meta:
        verbose_name, verbose_name_plural = (u'Etape', u'Etapes')
        
# Rôle de la FUTFactory
class Role(models.Model):
    # Attributs
    name = models.CharField(u'Nom', max_length=650, unique=True)
    description = models.TextField(u'Description', blank=True)
    
    # Méthodes
    def __unicode__(self):
        return u'%s' % (self.name)
    
    # Meta
    class Meta:
        verbose_name, verbose_name_plural = (u'Rôle de la FUTFactory', u'Rôles de la FUTFactory')

# Type de FUT
class Type(models.Model):
    # Attributs
    name = models.CharField(u'Nom', max_length=650, unique=True)
    description = models.TextField(u'Description', blank=True)
    
    # Méthodes
    def __unicode__(self):
        return u'%s' % (self.name)
    
    # Meta
    class Meta:
        verbose_name, verbose_name_plural = (u'Type de FUT', u'Types de FUT')

# Domaine de FUT
class Domain(models.Model):
    # Attributs
    name = models.CharField(u'Nom', max_length=650, unique=True)
    description = models.TextField(u'Description', blank=True)
    
    # Méthodes
    def __unicode__(self):
        return u'%s' % (self.name)
    
    # Meta
    class Meta:
        verbose_name, verbose_name_plural = (u'Domaine de FUT', u'Domaines de FUT')

# Type de clients cibles du FUT
class TargetCustomersType(models.Model):
    # Attributs
    name = models.CharField(u'Nom', max_length=650, unique=True)
    description = models.TextField(u'Description', blank=True)
    
    # Méthodes
    def __unicode__(self):
        return u'%s' % (self.name)
    
    # Meta
    class Meta:
        verbose_name, verbose_name_plural = (u'Type de clients cibles du FUT', u'Types de clients cibles du FUT')
        
# Type d'acteur du FUT
class ActorType(models.Model):
    # Attributs
    name = models.CharField(u'Nom', max_length=650, unique=True)
    description = models.TextField(u'Description', blank=True)
    
    # Méthodes
    def __unicode__(self):
        return u'%s' % (self.name)
    
    # Meta
    class Meta:
        verbose_name, verbose_name_plural = (u'Type d\'acteur du FUT', u'Types d\'acteur du FUT')

# Acteur du FUT
class Actor(models.Model):
    # Attributs
    first_name = models.CharField(u'Prénom(s)', max_length=250)
    last_name = models.CharField(u'Nom', max_length=250)
    email = models.EmailField(u'E-mail', blank=True)
    actor_type = models.ForeignKey(ActorType, verbose_name=u'Type d\'acteur')
    comments = models.TextField(u'Commentaires', blank=True)
    
    # Méthodes
    def save(self, *args, **kwargs):
        self.first_name = self.first_name.capitalize()
        self.last_name = self.last_name.upper()
        super(Actor, self).save(*args, **kwargs)
    
    def get_full_name(self):
        return u'%s %s' % (self.first_name, self.last_name)
    get_full_name.short_description = u'Prénom(s) et Nom'
    get_full_name.admin_order_field = 'last_name'

    def __unicode__(self):
        return self.get_full_name()
    
    # Meta
    class Meta:
        verbose_name, verbose_name_plural = (u'Acteur', u'Acteurs')

# FUT
class FUT(models.Model):
    # Attributs
    name = models.CharField(u'Nom', max_length=650)
    description = models.TextField(u'Description')
    target_customers = models.ManyToManyField(TargetCustomersType, verbose_name=u'Clients cibles', blank=True, null=True)
    scheduled_start_date = models.DateField(u'Date de début prévue', blank=True, null=True)
    effective_start_date = models.DateField(u'Date de début effective', blank=True, null=True)
    scheduled_end_date = models.DateField(u'Date de fin prévue', blank=True, null=True)
    effective_end_date = models.DateField(u'Date de fin effective', blank=True, null=True)
    expected_number_of_futers = models.PositiveIntegerField(u'Nombre de FUTeurs souhaité', blank=True, null=True)
    effective_number_of_futers = models.PositiveIntegerField(u'Nombre de FUTeurs effectif', blank=True, null=True)
    fut_type = models.ForeignKey(Type, verbose_name=u'Type de FUT', blank=True, null=True)
    domain = models.ForeignKey(Domain, verbose_name=u'Domaine')
    release_manager = models.ForeignKey(Actor, verbose_name=u'Release Manager', related_name='release_managed_futs', blank=True, null=True)
    role_ff = models.ForeignKey(Role, verbose_name=u'Rôle de la FUTFactory', blank=True, null=True)
    state = models.ForeignKey(Step, verbose_name=u'Etat d\'avancement')
    leader =  models.ForeignKey(Actor, verbose_name=u'Leader FUTFactory', related_name='managed_futs', blank=True, null=True)
    support =  models.ForeignKey(Actor, verbose_name=u'Support FUTFactory', related_name='half_managed_futs', blank=True, null=True)
    comments = models.TextField(u'Commentaires', blank=True)
    sharing_doc_space = models.ForeignKey(Folder, verbose_name='Espace de partage documentaire')
    
    # Méthodes
    def save(self, *args, **kwargs):
        if not self.pk:
            root = Folder.objects.create(name='%s' % (self.name), description='Espace de partage documentaire du FUT : %s' % (self.name))
            root.save()
            self.sharing_doc_space = root
        super(FUT, self).save(*args, **kwargs)
        
    def __unicode__(self):
        return u'%s' % (self.name)
    
    @models.permalink
    def get_absolute_url(self):
        return ('fut-detail', [str(self.id)])
    
    def get_full_target_customers(self):
        if len(self.target_customers.all()) > 0:
            tc_string = self.target_customers.all()[0].__unicode__()
            for i in range(1, len(self.target_customers.all())):
                tc_string += "/" + self.target_customers.all()[i].__unicode__()
            return smart_unicode(tc_string)
        else:
            return u''
    get_full_target_customers.short_description = u'Clients cibles'

    # Meta
    class Meta:
        verbose_name, verbose_name_plural = (u'FUT', u'FUTs')