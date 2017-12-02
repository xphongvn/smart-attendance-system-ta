# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse

from bson.json_util import dumps
from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017')
db = client['ta_sas']
UserClassifyIdCollection = db['UserClassifyId']

# Create your views here.


def studentList(request):
    students = list(UserClassifyIdCollection.find())
    response = HttpResponse(dumps(students, sort_keys=True), content_type="application/json")
    response['Access-Control-Allow-Origin'] = 'http://localhost:3000'
    return response
