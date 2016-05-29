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
    if route_table_result['results'] == []:
        return HttpResponseNotFound('<h1>Page not found</h1>')
    else:
        no_of_customers=route_table_result['results'][0]['custCount']
        print(no_of_customers)
    
        from_addr=route_table_result['results'][0]['from']
        to_addr=route_table_result['results'][0]['to']
        full_route=from_addr + " to " + to_addr
        print (full_route)
        if full_route == routename:
            if "custmMessage" in route_table_result['results'][0]:
                print("custmMessage there")
                cust_message=route_table_result['results'][0]['custmMessage']
            else:
                cust_message="Your route "+ routename + " is now open"        
            return render_to_response("routepage.html", {"routename":routename, "routeid":routeid, "no_of_customers":no_of_customers, "cust_message": cust_message}, context_instance=RequestContext(request))

        else :
            return HttpResponseNotFound('<h1>Page not found</h1>')


def customerjoin(request, routeid, routename):
    customer_phone=request.POST['mobile']    
    connection = http.client.HTTPSConnection('api.parse.com', 443)
    params = urllib.parse.urlencode({"where":json.dumps({
           "userPhone":customer_phone,
           "routeId":routeid
         })})
    connection.connect()
    connection.request('GET', '/1/classes/RouteJoin?%s' % params, '', {
           "X-Parse-Application-Id": "IBArnAuw83Th0SfDmF55VdMUgsNXFiL2TuC6qwiC",
           "X-Parse-REST-API-Key": "2coKSQ3ZGvWRJW3ZVReOs7ETy4rXiMP2i54eTO4N"
         })
    myresult=json.loads(connection.getresponse().read().decode())
    print (myresult)
    if myresult['results'] == []:
        connection.request('POST', '/1/classes/RouteJoin', json.dumps({
               "userPhone":customer_phone,
               "routeId":routeid
             }), {
            "X-Parse-Application-Id": "IBArnAuw83Th0SfDmF55VdMUgsNXFiL2TuC6qwiC",
            "X-Parse-REST-API-Key": "2coKSQ3ZGvWRJW3ZVReOs7ETy4rXiMP2i54eTO4N"
        })

        
#        the_objid = (myresult['results'][0]['objectId'])
        connection = http.client.HTTPSConnection('api.parse.com', 443)
        connection.connect()
        connection.request('PUT', '/1/classes/Route/'+routeid, json.dumps({
               "custCount": {
                 "__op": "Increment",
                 "amount": 1
               }
             }), {
               "X-Parse-Application-Id": "IBArnAuw83Th0SfDmF55VdMUgsNXFiL2TuC6qwiC",
               "X-Parse-REST-API-Key": "2coKSQ3ZGvWRJW3ZVReOs7ETy4rXiMP2i54eTO4N",
               "Content-Type": "application/json"
             })

        msg='Dear customer , your booking is confirmed. Driver details will be shared shortly. Thank You. Visit us at utoorides.com or call 8884615615'        
        data =  urllib.parse.urlencode({'username': 'sweekar07@yahoo.com', 'hash': '24a69c12340e221b4095b87d65b2e79b27999932', 'numbers': customer_phone, 'message' : msg, 'sender': 'UTOORD'})
        data = data.encode('utf-8')
        request = urllib.request.Request("http://api.textlocal.in/send/?")
        f = urllib.request.urlopen(request, data)
        fr = f.read()
        print (fr)
        return HttpResponseRedirect("/"+routeid+"/"+routename+"/")

    else:
        return HttpResponseRedirect("/"+routeid+"/"+routename+"/")
