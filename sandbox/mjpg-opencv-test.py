import cv2
import sys

cascPath = 'haarcascade_frontalface_alt.xml'
faceCascade = cv2.CascadeClassifier(cascPath)

print(faceCascade)

cap = cv2.VideoCapture('http://192.168.1.237:8080/?action=stream&ignored.mjpg')
cap.set(3, 640) #WIDTH
cap.set(4, 480) #HEIGHT

while True:
  ret, frame = cap.read()
  gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

  faces = faceCascade.detectMultiScale(
    gray,
    scaleFactor=1.1,
    minNeighbors=5,
    minSize=(30, 30),
    flags=cv2.CASCADE_SCALE_IMAGE
  )

  for (x, y, w, h) in faces:
    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
    text = str(x + w/2) + ", " + str(y + h/2)
    cv2.putText(frame, text, (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 255), 2)

    # Display the resulting frame
  cv2.imshow('Video', frame)

  if cv2.waitKey(1) == 27:
    exit(0)