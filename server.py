from copyreg import pickle
import socket
import sys
import pickle

import json
import face_recognition
import cv2
import numpy as np
import msgpack
import msgpack_numpy as m



known_face_encodings = [

]
known_face_names = [

]

# Initialize some variables
face_locations = []
face_encodings = []
face_names = []
process_this_frame = True

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_address = ('0.0.0.0',4000)
s.bind(server_address)
s.listen()
conn, addr = s.accept()
print("Do Ctrl+c to exit the program !!")

while True:
    print("####### Server is listening #######")
    
    frame = conn.recv(1000000)
    frame = msgpack.unpackb(frame, object_hook=m.decode)

    # print(frame)
    # frame = np.fromstring(frame, dtype=np.float64)


    #print("\n\n 2. Server received: ", data.decode('utf-8'), "\n\n")


    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

        # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
    rgb_small_frame = small_frame[:, :, ::-1]
        
        # Find all the faces and face encodings in the current frame of video
    face_locations = face_recognition.face_locations(rgb_small_frame)
    face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

    face_names = []
    for idx,face_encoding in enumerate(face_encodings):
            # See if the face is a match for the known face(s)
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding,tolerance=0.4)
            name = "Unknown"

            # If a match was found in known_face_encodings, just use the first one.
            if True in matches:
                first_match_index = matches.index(True)
                name = known_face_names[first_match_index]
                print(f"Face Identified: {name}")

            else:
                name = input("Enter name: ")
                known_face_encodings.append(face_encodings[idx])
                known_face_names.append(name)
            face_names.append(name)
    












    conn.sendall(json.dumps([face_locations, face_names]).encode())