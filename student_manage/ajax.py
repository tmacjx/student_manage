# coding=utf-8
"""
  author:wk
  api:1.0
  date:2016/03/12

"""
from util.functions import json_response


def index(request):
    result = {"status": 0, "apiVersion": "1.0", "msg": "", "data": {}}
    return json_response(result)