from unittest import TestCase
from django.test.client import Client

from people.models import *

class ModelSmokeTest(TestCase):

  def test_model(self):
    # garantindo que o banco esta vazio
    self.assertEquals(Usuario.objects.count(), 0)

    usuario = Usuario(email = "flavio.cdc@gmail.com")
    usuario.save()
    self.assertEquals(Usuario.objects.count(), 1)

    agenda = Agenda.objects.create(usuario = usuario)
    
    # testando que o relacionamento Usuario<->Agenda funciona
    self.assertEquals(usuario.agenda, agenda)

    # testando que nao exista nenhum contato
    self.assertEquals(usuario.agenda.contatos.count(), 0)
    usuario.agenda.contatos.create(nome="Gabi", telefone="123")
  
    # deve possuir um contato agora
    self.assertEquals(usuario.agenda.contatos.count(), 1)

class SincronizarContatos(TestCase):
  def setUp(self):
    self.client = Client();

  def test_sincronizar(self):
    response = self.client.get('/api/sincronizar/flavio.cdc@gmail.com')
    self.assertEquals(response.status_code, 200)
