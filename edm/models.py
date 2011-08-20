# -*- coding: UTF-8 -*- #
from django.db import models

# Répertoire (espace documentaire)
class Folder(models.Model):
    # Attributs
    name = models.CharField(u'Nom', max_length=650)
    description = models.TextField(u'Description', blank=True)
    parent_folder = models.ForeignKey('self', related_name='subfolders', verbose_name='Répertoire parent', null=True, blank=True)
    
    # Méthodes
    def __unicode__(self):
        return u'%s' % (self.name)
    
    # Meta
    class Meta:
        verbose_name, verbose_name_plural = (u'Répertoire', u'Répertoires')
        unique_together = ('name','parent_folder')

# Document
class Document(models.Model):
    # Attributs
    name = models.CharField(u'Nom', max_length=650)
    description = models.TextField(u'Description', blank=True)
    folder = models.ForeignKey(Folder, verbose_name=u'Répertoire', related_name='documents')
    
    # Méthodes 
    def __unicode__(self):
        return u'%s' % (self.name)
    
    # Meta
    class Meta:
        verbose_name, verbose_name_plural = (u'Document', u'Documents')
        unique_together = ('name','folder')

# Fichier
class File(models.Model):
    # Attributs
    file = models.FileField(u'Fichier', upload_to='fut_documents')
    version = models.CharField(u'Version', max_length=5)
    document = models.ForeignKey(Document, verbose_name='Document')
    
    # Méthodes 
    def __unicode__(self):
        return u'%s' % (self.name)
    
    # Meta
    class Meta:
        verbose_name, verbose_name_plural = (u'Fichier', u'Fichiers')
        unique_together = ('version','document')
                
    