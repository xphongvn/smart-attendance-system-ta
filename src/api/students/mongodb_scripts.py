from pymongo import MongoClient
import random

id_name = ["Alec", "Emil", "Greg", "Phong", "Thinh"]
photo_url = ["https://image.ibb.co/mPMU7m/Alec_0.jpg",
             "https://image.ibb.co/ccA0DR/Emil_4.jpg",
             "https://image.ibb.co/ixsQf6/Greg_3.jpg",
             "https://image.ibb.co/miKexm/Phong_8.png",
             "https://image.ibb.co/eXA8q6/Thinh_2.png"]

# Connect to MongoDb
client = MongoClient('mongodb://localhost:27017')
db = client['ta_sas']

# Insert to UserClassifyId Database
# Drop this database if exist
db.drop_collection('UserClassifyId')

# Push to this database name and id
db_to_push = db['UserClassifyId']

for i in xrange(len(id_name)):
    post = {"userName": id_name[i],
            "classifyId": i,
            "photo": photo_url[i],
            "status": "out" if random.random() > 0.5 else "in"}
    post_id = db_to_push.insert_one(post).inserted_id
    print(post_id)

###############################################################################
# Create fake Check-in
# Drop this database if exist
db.drop_collection('CheckInLog')

# Push to this database some fake check in data
db_to_push = db['CheckInLog']

post = { "userName" : "Phong",
         "classifyId": 3,
         "type" : "in",
         "location" : "Tokyo Academics",
         "createdAt" : 1511672254.04792}
post_id = db_to_push.insert_one(post).inserted_id
print(post_id)

post = {"userName" : "Greg",
        "classifyId": 2,
        "type" : "in",
        "location" : "Tokyo Academics",
        "createdAt" : 1511672267.02381}
post_id = db_to_push.insert_one(post).inserted_id
print(post_id)

post = {"userName" : "Alec",
        "classifyId": 0,
        "type" : "in",
        "location" : "Tokyo Academics",
        "createdAt" : 1511672276.36018}

post_id = db_to_push.insert_one(post).inserted_id
print(post_id)

post = {"userName" : "Thinh",
        "classifyId": 4,
        "type" : "in",
        "location" : "Tokyo Academics",
        "createdAt" : 1511672276.3994}

post_id = db_to_push.insert_one(post).inserted_id
print(post_id)