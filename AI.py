''' collects required packages '''

import face_recognition
import numpy as np
import cv2
import csv
import os
from datetime import datetime

''' sets up the camera '''
video_capture = cv2.VideoCapture(0)

''' creates images and converts them '''
kavya_image = face_recognition.load_image_file("kavya.jpg")
kavya_encoding = face_recognition.face_encodings(kavya_image)[0]

dhinesh_image = face_recognition.load_image_file("dhinesh.jpg")
dhinesh_encoding = face_recognition.face_encodings(dhinesh_image)[0]

mohnish_image = face_recognition.load_image_file("mohnish.jpg")
mohnish_encoding = face_recognition.face_encodings(mohnish_image)[0]

prabha_image = face_recognition.load_image_file("prabha.jpg")
prabha_encoding = face_recognition.face_encodings(prabha_image)[0]

shanmu_image = face_recognition.load_image_file("shanmu.jpg")
shanmu_encoding = face_recognition.face_encodings(shanmu_image)[0]



''' list of known faces '''
known_face_encoding = [
kavya_encoding,
dhinesh_encoding,
mohnish_encoding,
prabha_encoding,
shanmu_encoding
]

''' list of known names '''
known_face_names = [
"Kavya",
"Dhinesh",
"Mohnish Swarup",
"Prabha",
"Shanmuga Priya",
]

students = known_face_names.copy()

face_locations = []
face_encodings = []
face_names = []
s = True

now = datetime.now()
current_date = now.strftime("%Y/%m/%d")

''' creates an attendance sheet '''

f = open(r'Attendance.csv', 'w+',newline = '')
lnwriter = csv.writer(f)
lnwriter.writerow(["Name", "Date", "Time"])
while True:
    _,frame = video_capture.read()
    small_frame = cv2.resize(frame, (0,0),fx=0.25, fy=0.25)
    rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)
    if s:
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
        face_names = []
        for face_encoding in face_encodings:
            matches = face_recognition.compare_faces(known_face_encoding, face_encoding)
            name = ""
            face_distance = face_recognition.face_distance(known_face_encoding, face_encoding)
            best_match_index = np.argmin(face_distance)
            if matches[best_match_index]:
                name = known_face_names[best_match_index]

                face_names.append(name)
                if name in known_face_names:
                    if name in students:
                        students.remove(name)
                        print(students)
                        current_time = now.strftime("%H:%M:%S")
                        lnwriter.writerow([name, current_date, current_time])
    cv2.imshow("attendance system", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
video_capture.release()
cv2.destroyAllWindows()
f.close()
