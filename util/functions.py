# coding=utf-8
from django.http import HttpResponse
import simplejson as json


json_response = lambda x: HttpResponse(
    json.dumps(x, ensure_ascii=False),
    content_type='application/json; charset=utf-8')