import openface
import cv2
import os
import pickle
import numpy as np
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import GridSearchCV
from sklearn.svm import SVC

id_name = ["Alec", "Greg", "Phong"]


def train(features, labels):
    # prepare the labels for a training process
    label = LabelEncoder().fit(labels)
    label_num = label.transform(labels)
    # some parameters for the trained model
    param_grid = [
        {'C': [1, 10, 100, 1000],
         'kernel':['linear']},
        {'C': [1, 10, 100, 1000],
         'gamma':[0.001, 0.0001],
         'kernel':['rbf']}
    ]

    # construct the model
    clf = GridSearchCV(SVC(C=1, probability=True), param_grid, cv=5)

    # train the model
    clf.fit(features, label_num)

    # store the model
    f_name = "../../resource/svm.pkl"
    print("Saving classifier to '{}'".format(f_name))
    with open(f_name, 'w') as f:
        pickle.dump((label, clf), f)


# function to calculate the feature representation of the face
def get_rep(img_path, align, net, multiple=False):
    # load the image from the path
    bgr_img = cv2.imread(img_path)
    if bgr_img is None:
        raise Exception("Unable to load the image: {}".format(img_path))
    # convert to rgb
    rgb_img = cv2.cvtColor(bgr_img, cv2.COLOR_BGR2RGB)

    # there could be possible multiple images in the face
    if multiple:
        bbs = align.getAllFaceBoundingBoxes(rgb_img)
    else:
        bb1 = align.getLargestFaceBoundingBox(rgb_img)
        bbs = [bb1]
    if len(bbs) == 0 or (not multiple and bb1 is None):
        raise Exception("Unable to find a face: {}".format(img_path))
    # array to hold the feature representations of the faces
    reps = []

    # iterate over the faces that are found
    for bb in bbs:
        # align the face before feature calculation
        aligned_face = align.align(
            96,
            rgb_img,
            bb,
            landmarkIndices=openface.AlignDlib.OUTER_EYES_AND_NOSE
        )
        if aligned_face is None:
            raise Exception("Unable to align image: {}".format(img_path))

        # get the feature representation from the deep learning network
        rep = net.forward(aligned_face)
        # append this representation to the array
        reps.append(rep)

    # cast everything to a proper numpy array
    s_reps = np.array(reps)

    return s_reps


def make_classifier(all_faces_dir, align, net):
    # get all folders in output
    faces_dir = [o for o in os.listdir(all_faces_dir) if os.path.isdir(os.path.join(all_faces_dir, o))]

    features = None
    labels = []
    first_loop = True

    for face_dir in faces_dir:
        name = face_dir # folder name is the person's name
        id_counter = id_name.index(name)  # for training the classifier we can only use integer

        # build the folder path
        face_dir_path = os.path.join(all_faces_dir, face_dir)
        # get images in folder
        face_dir_images = [o for o in os.listdir(face_dir_path) if os.path.isfile(os.path.join(face_dir_path, o))]
        # iterate through all images in a folder
        for face_dir_image in face_dir_images:
            # build the proper image path
            face_dir_image_path = os.path.join(face_dir_path, face_dir_image)
            print face_dir_image_path

            # get the feature representations for the image
            reps = get_rep(face_dir_image_path, align, net)

            # append the feature of the array going to be returned
            if first_loop:
                features = reps
                first_loop = False
            else:
                features = np.concatenate([features, reps])

            # same for the labels
            labels.append(id_counter)

    # pass everything to the train function
    train(features, labels)


# path to the face alignment model
dLib_predictor = "../../resource/shape_predictor_68_face_landmarks.dat"
# construct the face alignment model
align = openface.AlignDlib(dLib_predictor)
# path to deep neural network for feature representation
network_model = "../../resource/nn4.small2.v1.t7"
# construct the network for feature represenation
net = openface.TorchNeuralNet(network_model, 96)

make_classifier("../../output", align, net)
