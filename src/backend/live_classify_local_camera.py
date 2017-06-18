import openface
import numpy as np
import os
import cv2
import pickle

id_name = ["Alec", "Greg", "Phong", "Emil"]


def classify(aligned_face, net, clf, le):
    rep = net.forward(aligned_face)
    predictions = clf.predict_proba(rep.reshape((1, len(rep)))).ravel()
    maxI = np.argmax(predictions)
    person = le.inverse_transform(maxI)
    confidence = predictions[maxI]
    print("Predict {} with {:.2f} confidence.".format(person, confidence))
    return person

# path to the face alignment model
dLib_predictor = "../../resource/shaqpe_predictor_68_face_landmarks.dat"
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
            print("Found {} face".format(len(bbs)))
            for bb2 in bbs:
                alignedFace = align.align(96, cameraFrame, bb2,
                                            landmarkIndices=openface.AlignDlib.OUTER_EYES_AND_NOSE)
                id = classify(alignedFace, net, clf, le)
                person_name = id_name[id]
                print(person_name)

                rectColor = (0,255, 0)
                textColor = (255, 0, 0)
                face_top_left = (bb2.left(), bb2.top())
                face_bottom_right = (bb2.right(), bb2.bottom())
                cv2.rectangle(cameraFrame, face_top_left, face_bottom_right, rectColor)
                cv2.putText(cameraFrame, person_name, face_top_left,
                        fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=1, color=textColor, thickness=2)

            cv2.imshow('FaceRecognizer', cameraFrame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        except:
            cv2.imshow('FaceRecognize', cameraFrame)
            continue
