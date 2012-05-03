# -*- coding: utf-8 -*-
import json

from django.http import HttpResponse

class JsonHttpResponse(HttpResponse):
    def __init__(self, data=None, status=None, content_type='application/json'):
        self.data_dict = data
        content = json.dumps(data)

        super(JsonHttpResponse, self).__init__(content=content,
                                               status=status,
                                               content_type=content_type)

    def reload_content(self):
        self.content = json.dumps(self.data_dict)

