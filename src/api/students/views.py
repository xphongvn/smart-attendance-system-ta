# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse

from bson.json_util import dumps
from pymongo import MongoClient
from bson.objectid import ObjectId

client = MongoClient('mongodb://localhost:27017')
db = client['ta_sas']
UserClassifyIdCollection = db['UserClassifyId']

# Create your views here.

def mapObject(obj):
    obj['_id'] = str(obj.get('_id'))
    return obj

def studentList(request):
    students = list(UserClassifyIdCollection.find())
    convertedStudents = list(map(mapObject, students))
    response = HttpResponse(dumps(convertedStudents, sort_keys=True), content_type="application/json")
    response['Access-Control-Allow-Origin'] = 'http://localhost:3000'
    return response

def getStudent(request, student_id):
    student = UserClassifyIdCollection.find_one({"_id":ObjectId(student_id)})
    response = HttpResponse(dumps(mapObject(student), sort_keys=True), content_type="application/json")
    response['Access-Control-Allow-Origin'] = 'http://localhost:3000'
    return response