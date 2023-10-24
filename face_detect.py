import cv2
import numpy as np
import face_recognition
import os
import glob
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import retrivedata as data



def check_for_new_image(folder_path):
    # Get a list of image files in the folder (you can adjust the file extensions as needed)
    image_files = glob.glob(os.path.join(folder_path, '*.jpg'))  # Change '*.jpg' to the desired file extension
    if not image_files:
        return False, None
    # Get the latest modified time among the image files
    latest_image = max(image_files, key=os.path.getmtime)
    # Get the current date and time
    current_time = os.path.getmtime(latest_image)
    # Compare the modification time of the latest image with the current time
    if current_time > os.path.getmtime(folder_path):
        return True, latest_image
    else:
        return False, None


def findEndcodings(images):
    encodeList = []
    for img in images:
        img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)
    return encodeList
def checkface():
    path = r'facepath'
    images = []
    classnames = []
    mylist = os.listdir(path)
    print(mylist)
    count = len(mylist)
    for cl in mylist:
        curImg = cv2.imread(f'{path}/{cl}')
        images.append(curImg)
        classnames.append(os.path.splitext(cl)[0])
    print(classnames)
    encodeList = findEndcodings(images)
    print('Encodding Complete')
    print(len(encodeList))
    if len(encodeList) == 0:
        print('No images found')
        exit()
    cap = cv2.VideoCapture(0)

    while True:
        mylist = os.listdir(path)
        count_new = len(mylist)
        
        success, img = cap.read()
        imgS = cv2.resize(img,(0,0),None,0.25,0.25)
        imgS = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        
        if count_new > count:
            count = count_new 
            has_new_image, latest_image_path = check_for_new_image(path)
            if has_new_image:
                img_new = cv2.imread(latest_image_path) 
                img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
                file_name, _ = os.path.splitext(os.path.basename(latest_image_path))
                classnames.append(file_name)
                encode = face_recognition.face_encodings(img)[0]
                encodeList.append(encode)
                print(classnames)
                print(len(encodeList))

        faceLocFrame = face_recognition.face_locations(imgS)
        encodeFrame = face_recognition.face_encodings(imgS,faceLocFrame)

        for encodeFace,faceLoc in zip(encodeFrame,faceLocFrame):
            matches = face_recognition.compare_faces(encodeList, encodeFace,tolerance=0.44)
            faceDis = face_recognition.face_distance(encodeList, encodeFace)
            matchIndex = np.argmin(faceDis)
            if matches[matchIndex]:
                name = classnames[matchIndex].upper()
                return name
            else:
                return None

        cv2.imshow('frame',img)
        k = cv2.waitKey(1)
        if k == ord('q'):
            break
def compare():
    QRID = checkface()
    if QRID == None:
        print("Khuon mat khong co trong database.")
    else:
        mydb = data.connect_database()
        mycursor = mydb.cursor()
        mycursor.execute("SELECT FacePath FROM yourtablename WHERE QRID = %s",(QRID,))
        myresult = mycursor.fetchall()
        result = list(myresult[0])
        return (result[0])

# mydb = data.connect_database()
# mycursor = mydb.cursor()
# QRID = 'EventA-abc124xyz'
# mycursor.execute("SELECT FacePath FROM yourtablename WHERE QRID = %s",(QRID,))
# myresult = mycursor.fetchall()
# result = list(myresult[0])  
# print(result[0])
    
if __name__ == '__main__':
    var = compare()
    if var == None:
        print("Xac minh khong thanh cong.\nQuy khach vui long check in.")
    else:
        print("Xac minh thanh cong.")
