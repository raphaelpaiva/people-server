# -*- coding: utf-8 -*-

from http import JsonHttpResponse

import datetime

def data_atual(request):
    """Webservice que retorna a data atual em um Json.
    """

    hoje = datetime.date.today()

    result = {
        'data_atual': hoje.strftime('%d/%m/%Y')
    }
    
    return JsonHttpResponse(result)
