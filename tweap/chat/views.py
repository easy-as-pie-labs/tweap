from django.views.generic import View
from django.http import HttpResponse
import json


class Messages(View):
    def post(self, request):
        return HttpResponse(json.dumps(""), content_type="application/json")


class NodeAPI(View):
    def post(self, request):
        return HttpResponse(json.dumps(""), content_type="application/json")