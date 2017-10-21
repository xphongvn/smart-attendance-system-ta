import openface
import numpy as np
import os
import cv2
import pickle
from pymongo import MongoClient
import time
import datetime

id_name = ["Alec", "Emil", "Greg", "Phong", "Thinh"]
confidence_level = [0] * len(id_name)
reg_times = [0] * len(id_name)
last_in = [0] * len(id_name)
last_time_clean = 0


def push_to_db(person_id):
    client = MongoClient('mongodb://localhost:27017')
    db = client['ta_sas']
    # Get the userId for the classifyId
    db_id = db['UserClassifyId']
    record = db_id.find_one({"classifyId":person_id})
    user_name = record['userName']

    # Content to push
    location = "Tokyo Academics"
    type = "in"
    created_at = time.time()
    post = {"userName": user_name,
            "location": location,
            "type": type,
            "createdAt": created_at}

    db_to_push = db['CheckInLog']
    post_id = db_to_push.insert_one(post).inserted_id
    print(post_id)

def classify(aligned_face, net, clf, le):
    rep = net.forward(aligned_face)
    predictions = clf.predict_proba(rep.reshape((1, len(rep)))).ravel()
    maxI = np.argmax(predictions)
    person = le.inverse_transform(maxI)
    confidence = predictions[maxI]
    #print("Predict {} with {:.2f} confidence.".format(person, confidence))
    return person, confidence

if __name__ == "__main__":

    CONFIDENCE_THRESHOLD = 0.0
    show_video = True
    # path to the face alignment model
    dLib_predictor = "../../resource/shape_predictor_68_face_landmarks.dat"
    # construct the face alignment model
    align = openface.AlignDlib(dLib_predictor)
    # path to deep neural network for feature representation
    network_model = "../../resource/nn4.small2.v1.t7"
    # construct the network for feature represenation
    net = openface.TorchNeuralNet(network_model, 96)

    classifier_model = "../../resource/svm.pkl"

    with open(classifier_model, 'r') as f:
        (le, clf) = pickle.load(f)
        print("Successfully loaded SVM model")
        video = cv2.VideoCapture(0)
        if video is None:
            exit()

        while True:
            # grab image
            ret, cameraFrame = video.read()
            if not ret:
                exit()
            try:
                bbs = align.getAllFaceBoundingBoxes(cameraFrame)
                #print("Found {} face".format(len(bbs)))
                for bb2 in bbs:
                    alignedFace = align.align(96, cameraFrame, bb2,
                                                landmarkIndices=openface.AlignDlib.OUTER_EYES_AND_NOSE)
                    id, confidence = classify(alignedFace, net, clf, le)
                    # If the confidence of the recognition is large enough
                    if float(confidence) >= CONFIDENCE_THRESHOLD:
                        current_time = time.time()
                        # Check if the previous recognition is close to current time
                        if (current_time - reg_times[id]) < 2 and \
                                (current_time - last_in[id] > 120 or last_in[id] == 0):
                            confidence_level[id] += 50
                            if confidence_level[id] > 80:
                                confidence_level[id] = 0
                                last_in[id] = current_time
                                push_to_db(id)
                                person_name = id_name[id]
                                converted_time = datetime.datetime.fromtimestamp(int(current_time)).strftime('%Y-%m-%d %H:%M:%S')
                                print(person_name + " has come in at: " + converted_time)
                        reg_times[id] = current_time

                    if show_video:
                        rectColor = (0,255, 0)
                        textColor = (255, 0, 0)
                        face_top_left = (bb2.left(), bb2.top())
                        face_bottom_right = (bb2.right(), bb2.bottom())
                        cv2.rectangle(cameraFrame, face_top_left, face_bottom_right, rectColor)
                        cv2.putText(cameraFrame, id_name[id], face_top_left,
                                fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=1, color=textColor, thickness=2)

                if show_video:
                    cv2.imshow('FaceRecognizer', cameraFrame)
                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        break
            except:
                if show_video:
                    cv2.imshow('FaceRecognize', cameraFrame)
                continue

            # reset confidence if person not seen for 2 minutes
            current_time = time.time()
            # Only reset every 30 secs.
            if (current_time - last_time_clean) > 30:
                for i in xrange(len(reg_times)):
                    if current_time - reg_times[i] > 240:
                        confidence_level[i] = 0
            print(confidence_level)