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
        if(request.session.get('graph',None) != None):
            del request.session['graph']
        if(request.session.get('projection',None) != None):
            del request.session['projection']
        if(request.session.get('minWeight',None) != None):
            del request.session['minWeight']
        if(request.session.get('graphData',None) != None):
            del request.session['graphData']
    filterTest = request.GET.get('filter',None)
    if(filterTest):
        G = None
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
        data = []
        for gData in graphData:
            data.append({'eczane' :gData.eczane,
                        'recete_no' :gData.recete_no,
                        'doktor_diploma_tescil_no' :gData.doktor_diploma_tescil_no,
                        'verilen_adet' :gData.verilen_adet,
                        'urun_id' :gData.urun_id,
                        'sgketkinkod' :gData.sgketkinkod,
                        'firma_id' :gData.firma_id,
                        'madde' :gData.madde})
        request.session['graphData'] = json.dumps(data)
    projectGraph = request.GET.get('project',None)
    if(projectGraph):
        firstNode = request.GET.get('firstNode',None)
        secondNode = request.GET.get('secondNode',None)
        projection = request.GET.get('projection',None)
        minWeight = request.GET.get('minWeight',None)
        graphData = request.session.get('graphData',None)
        gData =  json.loads(request.session.get('graphData',None))
        G = nx.Graph()
        graphData = []
        projectionList = []
        for dat in gData:
            sBilgi = SatisDokumBilgi.getObject(dat)
            graphData.append(sBilgi)
        for gData in graphData:
            val1 = None
            val2 = None
            if(firstNode == '0'):
                val1 = gData.doktor_diploma_tescil_no
            if(firstNode == '1'):
                val1 = gData.recete_no
            if(firstNode == '2'):
                val1 = gData.urun_id
            if(firstNode == '3'):
                val1 = gData.sgketkinkod
            if(firstNode == '4'):
                val1 = gData.firma_id
            if(secondNode == '0'):
                val2 = gData.doktor_diploma_tescil_no
            if(secondNode == '1'):
                val2 = gData.recete_no
            if(secondNode == '2'):
                val2 = gData.urun_id
            if(secondNode == '3'):
                val2 = gData.sgketkinkod
            if(secondNode == '4'):
                val2 = gData.firma_id
            G.add_edge(val1,val2)
            if(projection == '0'):
                projectionList.append(gData.doktor_diploma_tescil_no)
            if(projection == '1'):
                projectionList.append(gData.recete_no)
            if(projection == '2'):
                projectionList.append(gData.urun_id)
            if(projection == '3'):
                projectionList.append(gData.sgketkinkod)
            if(projection == '4'):
                projectionList.append(gData.firma_id)
        projectionList = list(set(projectionList))
        P = bipartite.weighted_projected_graph(G,projectionList)
        partData = list(P.edges.data())
        jsonData = json.dumps(partData)
        request.session['json_data'] =  jsonData
        request.session['first_node'] =  firstNode
        request.session['second_node'] =  secondNode
        request.session['projection'] =  projection
        request.session['minWeight'] =  minWeight
    pharmacyList = []
    firmList = []
    firstNode =  request.session.get('first_node')
    secondNode =  request.session.get('second_node')
    projection =  request.session.get('projection')
    minWeight =  request.session.get('minWeight')
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
            'jsonData':jsonGraphData,
            'eczaneListesi' : pharmacyList,
            'firmaListesi' : firmList,
            'eczaneId' : eczaneId,
            'firmaId' : firmaId,
            'firstNode' : firstNode,
            'secondNode' : secondNode,
            'projection' : projection,
            'min-weight': minWeight
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
