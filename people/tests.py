# -*- coding: utf-8 -*-

from django.test import TestCase
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


class UploadAgendaTestCase(TestCase):
    def setUp(self):
        self.client = Client();


    def test_upload_agenda_usuario_nao_cadastrado(self):
        """ Test upload da agenda de um usuário não cadastrado.
            Esperado: {'success': True}
        """

        url = reverse('upload_agenda', kwargs={'email': "teste@gmail.com"})
        contatos = [
            {'nome': u"Patrícia", 'telefone': "12345678"},
            {'nome': u"Pedro", 'telefone': "87654321"},
        ]

        response = self.client.post(url, {'contatos': json.dumps(contatos)})

        self.assertEquals(json.loads(response.content), {'success': True})

        # Deve ter sido criado 1 Usuário com 1 Agenda com 2 Contatos
        self.assertEquals(Usuario.objects.count(), 1)
        self.assertEquals(Usuario.objects.filter(email="teste@gmail.com").count(), 1)

        self.assertEquals(Agenda.objects.count(), 1)
        self.assertEquals(Agenda.objects.filter(usuario__email="teste@gmail.com").count(), 1)

        self.assertEquals(Contato.objects.count(), 2)
        self.assertEquals(Contato.objects.filter(agenda__usuario__email="teste@gmail.com").count(), 2)
        self.assertEquals(Contato.objects.filter(nome=u"Patrícia", telefone="12345678").count(), 1)
        self.assertEquals(Contato.objects.filter(nome=u"Pedro", telefone="87654321").count(), 1)


    def test_upload_agenda_usuario_cadastrado_sem_contatos(self):
        """ Test upload da agenda de um usuário cadastrado sem contatos.
            Esperado: {'success': True}
        """
        self.usuario = Usuario.objects.create(email="teste@gmail.com")
        Agenda.objects.create(usuario=self.usuario)

        url = reverse('upload_agenda', kwargs={'email': "teste@gmail.com"})
        contatos = [
            {'nome': u"Letícia", 'telefone': "22334455"},
        ]

        response = self.client.post(url, {'contatos': json.dumps(contatos)})

        self.assertEquals(json.loads(response.content), {'success': True})

        # Deve ter sido criado 2 Contatos para esse usuário
        self.assertEquals(Usuario.objects.count(), 1)
        self.assertEquals(Usuario.objects.filter(email="teste@gmail.com").count(), 1)

        self.assertEquals(Agenda.objects.count(), 1)
        self.assertEquals(Agenda.objects.filter(usuario__email="teste@gmail.com").count(), 1)

        self.assertEquals(Contato.objects.count(), 1)
        self.assertEquals(Contato.objects.filter(agenda__usuario__email="teste@gmail.com").count(), 1)
        self.assertEquals(Contato.objects.filter(nome=u"Letícia", telefone="22334455").count(), 1)



    def test_upload_agenda_usuario_cadastrado_com_agenda(self):
        """ Test upload da agenda de um usuário cadastrado com contatos.
            A agenda deverá ser substituída 
            Esperado: {'success': True}
        """
        self.usuario = Usuario.objects.create(email="teste@gmail.com")
        Agenda.objects.create(usuario=self.usuario)
        self.usuario.agenda.contatos.create(nome=u"Patrícia", telefone=u"12345678")
        self.usuario.agenda.contatos.create(nome=u"Pedro", telefone=u"87654321")

        url = reverse('upload_agenda', kwargs={'email': "teste@gmail.com"})
        contatos = [
            {'nome': u"Letícia", 'telefone': "22334455"},
        ]

        response = self.client.post(url, {'contatos': json.dumps(contatos)})

        self.assertEquals(json.loads(response.content), {'success': True})

        # Deve ter sido apagado os contatos antigos e criado o novo
        self.assertEquals(Usuario.objects.count(), 1)
        self.assertEquals(Usuario.objects.filter(email="teste@gmail.com").count(), 1)

        self.assertEquals(Agenda.objects.count(), 1)
        self.assertEquals(Agenda.objects.filter(usuario__email="teste@gmail.com").count(), 1)

        self.assertEquals(Contato.objects.count(), 1)
        self.assertEquals(Contato.objects.filter(agenda__usuario__email="teste@gmail.com").count(), 1)
        self.assertEquals(Contato.objects.filter(nome=u"Letícia").count(), 1)
        self.assertEquals(Contato.objects.filter(nome=u"Patrícia").count(), 0)




class DownloadAgendaTestCase(TestCase):
    def setUp(self):
        self.usuario = Usuario.objects.create(email="teste@gmail.com")
        Agenda.objects.create(usuario=self.usuario)
        self.usuario.agenda.contatos.create(nome=u"Patrícia", telefone=u"12345678")
        self.usuario.agenda.contatos.create(nome=u"Pedro", telefone=u"87654321")

        self.client = Client();


    def test_download_agenda_com_usuario_cadastrado_com_contatos(self):
        """ Test download da agenda de um usuário cadastrada com contatos.
            Esperado: Lista de contatos desse usuário.
        """
        url = reverse('download_agenda', kwargs={'email': self.usuario.email})
        response = self.client.get(url)

        self.assertEquals(response.status_code, 200)

        resultado_esperado = [
            {'nome': u"Patrícia", 'telefone': "12345678"},
            {'nome': u"Pedro", 'telefone': "87654321"},
        ]
        self.assertEquals(json.loads(response.content), resultado_esperado)


    def test_download_agenda_com_usuario_cadastrado_sem_contatos(self):
        """ Test download da agenda de um usuário cadastrada sem contatos.
            Esperado: Lista vazia.
        """
        usuario = Usuario.objects.create(email="outro@gmail.com")
        Agenda.objects.create(usuario=usuario)

        url = reverse('download_agenda', kwargs={'email': "outro@gmail.com"})
        response = self.client.get(url)

        self.assertEquals(response.status_code, 200)
        self.assertEquals(json.loads(response.content), [])


    def test_download_agenda_sem_usuario_cadastrado(self):
        """ Test download da agenda de um usuário não cadastrado.
            Esperado: 404
        """
        url = reverse('download_agenda', kwargs={'email': "outro@gmail.com"})
        response = self.client.get(url)

        self.assertEquals(response.status_code, 404)




