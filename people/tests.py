from unittest import TestCase
from django.test.client import Client

from django.core.urlresolvers import reverse

import json
from people.models import Usuario, Contato, Agenda

class ModelSmokeTest(TestCase):

    def test_model(self):
        # garantindo que o banco esta vazio
        self.assertEquals(Usuario.objects.count(), 0)

        usuario = Usuario.objects.create(email = "flavio.cdc@gmail.com")
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
        response = self.client.get(reverse('sincronizar', kwargs={'email': '/api/sincronizar/flavio.cdc@gmail.com'}))
        self.assertEquals(response.status_code, 200)


class UsuarioTestCase(TestCase):
    def setUp(self):
        self.usuario = Usuario.objects.create(email="flavio.cdc@gmail.com")
        self.client = Client();

    def test_get_contato(self):
        url = reverse('get_usuario', kwargs={'usuario_id': self.usuario.id})
        response = self.client.get(url)

        self.assertEquals(response.status_code, 200)

        var_json = json.loads(response.content)
        self.assertEquals(var_json, {'id': self.usuario.id, 'email': self.usuario.email})


class AgendaTestCase(TestCase):
    def setUp(self):
        self.usuario = Usuario.objects.create(email="flavio.cdc@gmail.com")
        self.agenda = Agenda.objects.create(usuario=self.usuario)
        self.client = Client();

    def test_get_agenda(self):
        url = reverse('get_agenda', kwargs={'agenda_id': self.agenda.id})
        response = self.client.get(url)

        self.assertEquals(response.status_code, 200)

        var_json = json.loads(response.content)
        self.assertEquals(var_json, {'id': self.agenda.id, 'usuario_id': self.agenda.usuario.id})


class ContatoTestCase(TestCase):
    def setUp(self):
        self.usuario = Usuario.objects.create(email="flavio.cdc@gmail.com")
        self.agenda = Agenda.objects.create(usuario=self.usuario)
        self.contato = Contato.objects.create(nome=u'Patricia', telefone="92301059", agenda=self.agenda)
        self.client = Client();

    def test_get_agenda(self):
        url = reverse('get_contato', kwargs={'contato_id': self.contato.id})
        response = self.client.get(url)

        self.assertEquals(response.status_code, 200)

        var_json = json.loads(response.content)
        self.assertEquals(var_json, {'id': self.contato.id, 'nome': self.contato.nome, 'telefone': self.contato.telefone, 'agenda_id': self.contato.agenda.id})



