# -*- coding: utf-8 -*-

from django.http import Http404
from django.shortcuts import get_object_or_404

from http import JsonHttpResponse

from people.models import Usuario, Agenda, Contato


def sincronizar(request, email):  
    raise Http404


def get_usuario(request, usuario_id):
    usuario = get_object_or_404(Usuario, id=usuario_id)
    return JsonHttpResponse(usuario.to_dict())


def get_agenda(request, agenda_id):
    agenda = get_object_or_404(Agenda, id=agenda_id)
    return JsonHttpResponse(agenda.to_dict())


def get_contato(request, contato_id):
    contato = get_object_or_404(Contato, id=contato_id)
    return JsonHttpResponse(contato.to_dict())


