"""
Definition of views.
"""

from django.shortcuts import render
from django.http import HttpRequest
from django.template import RequestContext
from datetime import datetime
from .models import SatisDokumBilgi
from django.views.generic import TemplateView, ListView
import csv
import networkx as nx
from networkx.algorithms import bipartite
import matplotlib.pyplot as plt
from django.core import serializers
import json

def home(request):
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
            'jsonData':jsonData
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
