from django.db import models

class Usuario(models.Model):
    email = models.EmailField(max_length=200)

    def __unicode__(self):
    	return self.email

class Agenda(models.Model):
    usuario = models.OneToOneField(Usuario)
    
    def __unicode__(self):
	return 'Agenda de ' + self.usuario.email

class Contato(models.Model):
    nome = models.CharField(max_length=200)
    telefone = models.CharField(max_length=200)
    agenda = models.ForeignKey(Agenda, related_name="contatos")

    def __unicode__(self):
    	return self.nome + ': '+ self.telefone


