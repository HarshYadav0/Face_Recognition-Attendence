# pip install cmake
# pip install face_recognition
# pip install opencv-python
# pip install numpy

import face_recognition
import cv2
import numpy as np
import csv
from datetime import datetime

video_capture = cv2.VideoCapture(0) # According to your camera

# Load Known Faces
# 
harshu_image = face_recognition.load_image_file("faces/harsh.jpg")
harshu_encodings = face_recognition.face_encodings(harshu_image)[0]

rohan_image = face_recognition.load_image_file("faces/harsh.jpg") 
rohan_encodings = face_recognition.face_encodings(rohan_image)[0]


known_face_encodings = [harshu_encodings, rohan_encodings]
known_face_names =   ["Harshu", "Rohan"]

# List of students

students = known_face_names.copy()

face_locations = []
face_encodings = []

# Get the current time and date

now = datetime.now()
current_date = now.strftime("%d-%m-%Y")

f = open(f"{current_date}.csv", "w+", newline="")
lnwriter = csv.writer(f)


while True:
    _, frame = video_capture.read()
    small_frame = cv2.resize(frame,(0,0), fx=0.25, fy=0.25)
    rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)


    # Recognition Faces
    face_locations = face_recognition.face_locations(rgb_small_frame)
    face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

    for face_encoding in face_encodings:
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
        face_distance = face_recognition.face_distance(known_face_encodings, face_encoding)
        best_match_index = np.argmin(face_distance)

        if (matches[best_match_index]):
            name = known_face_names[best_match_index]

        # Add the text if person is present 
        if name in known_face_names:
            font = cv2.FONT_HERSHEY_SIMPLEX
            bottomLeftCornerOfText = (10, 100)
            fontScale = 1.5
            fontColor = (255, 0, 0)
            thickness = 3
            LineType = 2
            cv2.putText(frame, name + "Present",bottomLeftCornerOfText, font, fontScale, fontColor, thickness, LineType )

            if name in students:
                students.remove(name)
                current_time = now.strftime("%H-%M-%S")
                lnwriter.writerow([name, current_time])

    cv2.imshow("Attendence", frame)
    if cv2.waitKey(1) & 0xFF == ord("q"):
         break

video_capture.release()
cv2.destroyAllWindows()
f.close()