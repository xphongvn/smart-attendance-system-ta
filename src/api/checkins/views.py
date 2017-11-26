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


def checkinList(request):
    checkins = list(CheckInLog.find())
    return HttpResponse(dumps(checkins, sort_keys=True), content_type="application/json")
