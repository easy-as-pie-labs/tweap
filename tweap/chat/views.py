from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
import json

@csrf_exempt
def api(request):
    return HttpResponse(json.dumps("it works!"), content_type="application/json")