from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, HttpResponseNotFound
from django.conf import settings
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
import urllib.request
import urllib.parse
import json,http.client
import datetime, os, re

# Create your views here.

def joinroute(request, routeid, routename):
    connection = http.client.HTTPSConnection('api.parse.com', 443)
    params = urllib.parse.urlencode({"where":json.dumps({
           "objectId":routeid
         })})
    connection.connect()
    connection.request('GET', '/1/classes/Route?%s' % params, '', {
           "X-Parse-Application-Id": "IBArnAuw83Th0SfDmF55VdMUgsNXFiL2TuC6qwiC",
           "X-Parse-REST-API-Key": "2coKSQ3ZGvWRJW3ZVReOs7ETy4rXiMP2i54eTO4N"
         })
    route_table_result=json.loads(connection.getresponse().read().decode())
    no_of_customers=int(route_table_result['results'][0]['numCustomers'])
    print(no_of_customers)
    from_addr=route_table_result['results'][0]['from']
    to_addr=route_table_result['results'][0]['to']
    full_route=from_addr + " to " + to_addr
    print (full_route)
    if full_route == routename:
        
        return render_to_response("routepage.html", {"routename":routename}, {"no_of_customers":no_of_customers}, context_instance=RequestContext(request))

    else :
        return HttpResponseNotFound('<h1>Page not found</h1>')
