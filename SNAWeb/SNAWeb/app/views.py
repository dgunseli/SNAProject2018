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
    jsonData = None
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
        if(request.session.get('ecz_id',None) != None):
            del request.session['ecz_id']
        if(request.session.get('firm_id',None) != None):
            del request.session['firm_id']
    filterTest = request.GET.get('filter',None)
    if(filterTest):
        queryCommand = "SELECT * FROM app_satisdokumbilgi WHERE"
        queryList = []
        startDateParam = request.GET.get('start',None)
        endDateParam = request.GET.get('end',None)
        eczaneIdParam = request.GET.get('eczane',None)
        firmaIdParam = request.GET.get('firma',None)
        if(startDateParam == None):
            startDate = datetime.date(1000,1, 1)
            request.session['date_start'] = None
        else:
            startDate = datetime.strptime(startDateParam, '%Y-%m-%d')
            request.session['date_start'] = startDate.strftime('%m-%d-%Y')
            queryList.append(" islem_tarihi::date >= to_date('%s', 'MM-DD-YYYY')" % startDate.strftime('%m-%d-%Y'))
        if(endDateParam == None):
            endDate = datetime.date(9999,1, 1)
            request.session['date_end'] = None
        else:
            endDate = datetime.strptime(endDateParam, '%Y-%m-%d')
            request.session['date_end'] = endDate.strftime('%m-%d-%Y')
            queryList.append(" islem_tarihi::date <= to_date('%s', 'MM-DD-YYYY')" % endDate.strftime('%m-%d-%Y'))
        if(eczaneIdParam != None and eczaneIdParam != ''):
            if(int(eczaneIdParam) > 0):
                queryList.append(" eczane = %d" % int(eczaneIdParam))
            request.session['ecz_id'] = int(eczaneIdParam)
        else:
            request.session['ecz_id'] = -1
        if(firmaIdParam != None and firmaIdParam != ''):
            if(int(firmaIdParam) > 0):
                queryList.append(" firma_id = %d" % int(firmaIdParam))
            request.session['firm_id'] = int(firmaIdParam)
        else:
            request.session['firm_id'] = -1
        for x in range(len(queryList)):
            filterCommand = queryList[x]
            if(x > 0):
                filterCommand = " AND" + filterCommand
            queryCommand = queryCommand + filterCommand
        graphData = SatisDokumBilgi.objects.raw(queryCommand)
        G = nx.Graph()
        urunIdList = []
        for gData in graphData:
            G.add_edge(gData.recete_no,gData.urun_id)
            urunIdList.append(gData.urun_id)
        P = bipartite.weighted_projected_graph(G,urunIdList)
        partData = list(P.edges.data())
        jsonData = json.dumps(partData)
    pharmacyList = []
    firmList = []
    firstNode =  request.session.get('first_node')
    secondNode =  request.session.get('second_node')
    dateStart =  request.session.get('date_start')
    dateEnd =  request.session.get('date_end')
    jsonGraphData = request.session.get('json_data')
    eczaneId = request.session.get('ecz_id')
    firmaId = request.session.get('firm_id')

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
    assert isinstance(request, HttpRequest)
    return render(request,
        'app/index.html',
        {
            'title':'Ana Sayfa',
            'dateStart':dateStart,
            'dateEnd':dateEnd,
            'jsonData':jsonData,
            'eczaneListesi' : pharmacyList,
            'firmaListesi' : firmList,
            'eczaneId' : eczaneId,
            'firmaId' : firmaId
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
