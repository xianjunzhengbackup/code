from django.http import HttpResponse,Http404
import datetime

def hello(request):
    return HttpResponse("hello world")

def current_datetime(request):
    now=datetime.datetime.now()
    resp="<html><body>current time is %s</body></html>\n"%now
    return HttpResponse(resp)

def current_date_plus_offset(request,offset):
    try:
        #int_offset=int(offset)
        int_offset=' '
    except :
        raise Http404()
    now=datetime.datetime.now()
    assert False
    offset_in_seconds=int_offset*3600
    now=now+datetime.timedelta(0,offset_in_seconds)
    resp="<html><body>current time is %s</body></html>\n"%now
    return HttpResponse(resp)