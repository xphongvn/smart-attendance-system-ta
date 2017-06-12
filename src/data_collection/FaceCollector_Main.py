import cv2, sys, os, time, logging

# Some constants
SCALE_FACTOR = 1.75
MIN_NEIGHBORS = 5
MIN_WIDTH = 80
MIN_HEIGHT = 80
IMAGE_WIDTH = 200
IMAGE_HEIGHT = 200
MIRROR = True
NUM_PICS_PER_USER = 10

def initialize_face_detector():
    global classifier, video

    classifier = cv2.CascadeClassifier()
    status = classifier.load("../../resource/haarcascade_frontalface_default.xml")
    if not status:
        raise Exception("Failed to load the Classifier")

    # Start video
    video = cv2.VideoCapture(0)


def start_process():
    print("Starting Process...")
    initialize_face_detector()
    # Make output folder if not currently existing
    output_dir = "../../output"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print("Created new Folder " + output_dir)
    # Get number of people to collect their face data
    users = int(raw_input("Enter Total Number of People to Collect Data For: "))
    user_names = []
    i = 0
    # Get the people's names
    while i < users:
        user_name = raw_input("Please enter Person number " + str(i+1) + "'s name")
        user_dir = output_dir + "/" + user_name
        if not os.path.exists(user_dir):
            os.makedirs(user_dir)
            print("Created new User Directory " + user_dir)
            user_names.append((user_name, user_dir))
            i += 1
        else:
            print("User Directory already exists, try another name")
            continue
    collect_face_data(user_names)


def collect_face_data(user_names):
    image_size = (IMAGE_WIDTH, IMAGE_HEIGHT)
    for user in user_names:
        raw_input("Are you ready to collect face data of " + user[0] + "? Press Enter to Continue...")
        image_index = 0
        while image_index < NUM_PICS_PER_USER:
            file_name = user[1] + "/" + user[0] + "_" + str(image_index) + ".png"
            print("Created Image " + str(image_index) + "out of" + str(NUM_PICS_PER_USER) + " for " + user[0])

            cameraFrame, faces = grab()

            for face in faces:
                # Face stores coordinates of top left of face and size in width and height
                crop_face = cameraFrame[face[1]: face[1]+face[3]:, face[0]: face[0] + face[2]]
                # Resize image
                crop_face = cv2.resize(crop_face, image_size)
                cv2.imshow(user[0] + ": press y to save image", crop_face)
                if cv2.waitKey(1) == ord("y"):
                    # If y key is pressed, save image
                    cv2.imwrite(file_name, crop_face)
                    image_index += 1
                    break

            time.sleep(0.2)

        # Clear all windows before new collection
        cv2.destroyAllWindows()


def grab():
    global classifier, video

    # Initialization of variables
    cameraFrame = None
    faces = []
    found = False
    while not found:
        print("Looking for face...")
        ret, cameraFrame = video.read()
        if not ret:
            print("System Error. Exiting.")
            exit()
        if MIRROR:
            cv2.flip(cameraFrame, 1)
        faces = classifier.detectMultiScale(cameraFrame,
                                            scaleFactor=SCALE_FACTOR,
                                            minNeighbors=MIN_NEIGHBORS,
                                            minSize=(MIN_WIDTH, MIN_HEIGHT),
                                            flags=cv2.CASCADE_SCALE_IMAGE)
        if len(faces) > 0:
            found = True
    return cameraFrame, faces


##### MAIN FUNCTION #####

start_process()
print("Goodbye")
