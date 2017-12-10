from django.shortcuts import render_to_response
from mitteilungen.models import Mitteilung
from django.http.response import HttpResponseRedirect, HttpResponse

# Create your views here.
def show_messages(request):
    messages = Mitteilung.objects.all().select_subclasses().order_by('-mitteilung_id')
    
   
    c ={
        'messages': messages
        }
        
    return render_to_response('mitteilungsboard.html', c)
 
def message_read(request, mitteilung_id):
    mitteilung = Mitteilung.objects.get(mitteilung_id=mitteilung_id)
    if mitteilung.gelesen:
        mitteilung.gelesen=False
    else:
        mitteilung.gelesen=True
    mitteilung.save()
    
    return HttpResponseRedirect('/Mitteilungsboard')

def calc_messages(request):
    messages = Mitteilung.objects.filter(gelesen=False).select_subclasses()
    total = len(messages)

    return HttpResponse(total)