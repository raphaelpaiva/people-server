# -*- coding: utf-8 -*-

from django.http import Http404
from django.shortcuts import get_object_or_404

import json

from http import JsonHttpResponse

from people.models import Usuario, Agenda, Contato


def upload_agenda(request, email):
    """ Cria o usuário se ele não existir e cria os contatos de acordo com o json recebido no parâmetro 'contatos'.
        Retorna um json com a variável success indicando status de sucesso. 
        Em caso de erro, no json retornado também é enviada a mensagem de erro no parâmetro 'error'.
        Exemplos de retorno:
            {'success': True}    
            {'success': False, 'error': 'Exceção X'}    
    """
    usuario, created = Usuario.objects.get_or_create(email=email)
    if created:
        Agenda.objects.create(usuario=usuario)

    result = {'success': True}

    #TODO validar os campos recebidos
    try:
        contatos = json.loads(request.POST.get('contatos'))
        usuario.upload_agenda(contatos)
    except Exception, e:
        result['success'] = False
        result['error'] = unicode(e)

    return JsonHttpResponse(result)


def download_agenda(request, email):
    """ Retorna uma lista de dicts com nome e telefone de contatos.
        Caso o usuário não exista retorna 404.
        Exemplo de retorno:
            [
                {'nome': u"Patrícia", 'telefone': "87654321"},
                {'nome': u"Pedro", 'telefone': "12345678"},
            ]
    """
    usuario = get_object_or_404(Usuario, email=email)
    return JsonHttpResponse(usuario.agenda_to_dict())



