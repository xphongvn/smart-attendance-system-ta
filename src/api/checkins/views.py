# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse

from bson.json_util import dumps
from pymongo import MongoClient

# Create your views here.

client = MongoClient('mongodb://localhost:27017')
db = client['ta_sas']
CheckInLog = db['CheckInLog']

def mapObject(obj):
    obj['_id'] = str(obj.get('_id'))
    return obj

def checkinList(request):
    query_params = request.GET.copy()
    print query_params
    if query_params:
        if query_params.get("classifyId"):
            id = int(query_params["classifyId"])
    query_params = {"classifyId":id}
    print(query_params)
    checkins = list(CheckInLog.find(query_params))
    checkinsMap = list(map(mapObject, checkins))
    return HttpResponse(dumps(checkinsMap, sort_keys=True), content_type="application/json")

