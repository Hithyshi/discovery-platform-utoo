from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
# Create your views here.

def joinroute(request, routeid, routename):
    return render_to_response("routepage.html", {"routename":routename}, context_instance=RequestContext(request))
