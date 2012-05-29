# -*- coding: utf-8 -*-

from django.db import models

class Usuario(models.Model):
    email = models.EmailField(max_length=200, unique=True)

    def __unicode__(self):
    	return self.email

    class Meta:
        app_label = 'people'
        ordering = ['email']


    def agenda_to_dict(self):
        """ Retorna uma lista de dicts com nome e telefone dos contatos da agenda desse usuário.
            Caso o usuário não possua contatos, será retornado uma lista vazia.
            Exemplo de retorno:
                [    
                    {'nome': u"Patricia", 'telefone': "12345678"},
                    {'nome': u"Pedro", 'telefone': "87654321"},
                ]
        """
        return [{'nome': c.nome, 'telefone': c.telefone} for c in self.agenda.contatos.all()]

    def upload_agenda(self, contatos):
        """ Substitui agenda atual pela recebida em contatos.
            contatos é uma lista de dicts com nome e telefone dos contatos.
            Exemplo de contatos:
                [    
                    {'nome': u"Patricia", 'telefone': "12345678"},
                    {'nome': u"Pedro", 'telefone': "87654321"},
                ]
        """
        self.agenda.contatos.all().delete()
        
        for c in contatos:
            self.agenda.contatos.create(**c)



class Agenda(models.Model):
    usuario = models.OneToOneField(Usuario)
    
    def __unicode__(self):
	    return 'Agenda de ' + self.usuario.email

    class Meta:
        app_label = 'people'



class Contato(models.Model):
    nome = models.CharField(max_length=200)
    telefone = models.CharField(max_length=200)
    agenda = models.ForeignKey(Agenda, related_name="contatos")

    def __unicode__(self):
    	return self.nome + ': '+ self.telefone

    class Meta:
        app_label = 'people'
        ordering = ['nome']




