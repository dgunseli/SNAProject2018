"""
Definition of views.
"""

from django.shortcuts import render
from django.http import HttpRequest
from django.template import RequestContext
from datetime import datetime
from .models import SatisDokumBilgi, EczaneBilgi, FirmaBilgi
from django.views.generic import TemplateView, ListView
import csv
import networkx as nx
from networkx.algorithms import bipartite
import matplotlib.pyplot as plt
from django.core import serializers
import json
from .helpers import *



def home(request):
    clearTest = request.GET.get('clearSession',None)
    if (clearTest):
        if(request.session.get('pharmacy_list',None) != None):
            del request.session['pharmacy_list']
        if(request.session.get('firm_list',None) != None):
            del request.session['firm_list']
        if(request.session.get('first_node',None) != None):
            del request.session['first_node']
        if(request.session.get('second_node',None) != None):
            del request.session['second_node']
        if(request.session.get('date_start',None) != None):
            del request.session['date_start']
        if(request.session.get('date_end',None) != None):
            del request.session['date_end']
        if(request.session.get('json_data',None) != None):
            del request.session['json_data']
    pharmacyList = []
    firmList = []
    firstNode =  request.session.get('first_node')
    secondNode =  request.session.get('second_node')
    dateStart =  request.session.get('date_start')
    dateEnd =  request.session.get('date_end')
    jsonGraphData = request.session.get('json_data')

    if(request.session.get('pharmacy_list',None) == None):
        pharmacyList = setPharmacySessionData(request)
        request.session['pharmacy_list'] = json.dumps(pharmacyList)
    else:
        pharmacyList =  json.loads(request.session.get('pharmacy_list'))
        pharmacyDecoded = []
        for pharm in pharmacyList:
            eBilgi = json.loads(pharm,object_hook = EczaneBilgi.as_EczaneBilgi)
            pharmacyDecoded.append(eBilgi)
        pharmacyList = pharmacyDecoded
    if(request.session.get('firm_list',None) == None):
        firmList = setFirmSessionData(request)
        request.session['firm_list'] =  json.dumps(firmList)
    else:
        firmList =  json.loads(request.session.get('firm_list'))
        firmListDecoded = []
        for frm in firmList:
            fBilgi = json.loads(frm,object_hook = FirmaBilgi.as_FirmaBilgi)
            firmListDecoded.append(fBilgi)
        firmList = firmListDecoded

    """Renders the home page."""
    graphData = SatisDokumBilgi.objects.filter(islem_tarihi__gte='2018-03-25')
    G = nx.Graph()
    urunIdList = []
    for gData in graphData:
        G.add_edge(gData.recete_no,gData.urun_id)
        urunIdList.append(gData.urun_id)
    P = bipartite.weighted_projected_graph(G,urunIdList)
    partData = list(P.edges.data())
    jsonData = json.dumps(partData)
    assert isinstance(request, HttpRequest)
    return render(request,
        'app/index.html',
        {
            'title':'Ana Sayfa',
            'year':datetime.now().year,
            'jsonData':jsonData,
            'eczaneListesi' : pharmacyList,
            'firmaListesi' : firmList
        })

def contact(request):
    """Renders the contact page."""
    assert isinstance(request, HttpRequest)
    return render(request,
        'app/contact.html',
        {
            'title':'Contact',
            'message':'Your contact page.',
            'year':datetime.now().year,
        })

def about(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(request,
        'app/about.html',
        {
            'title':'About',
            'message':'Your application description page.',
            'year':datetime.now().year,
        })
