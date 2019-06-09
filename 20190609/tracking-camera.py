import threading
import cv2
import sys
import socket
from queue import Queue


def networking(q):
    soc = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    soc.bind(('0.0.0.0', 1025))

    raspberry_ip = '192.168.1.237'

    ex_data = [-1, -1]

    while True:
        data, evt = q.get()

        if ex_data == data:
            evt.set()
            q.task_done()
            continue

        byte_data = bytearray()

        for i in data:
            byte_i = bytes(str(i).encode())
            byte_data.extend(byte_i)

        print(byte_data)

        soc.sendto(byte_data, (raspberry_ip, 1025))

        evt.set()
        q.task_done()

        ex_data = data

    return -1


def imaging(q):
    cascPath = 'haarcascade_frontalface_alt.xml'
    faceCascade = cv2.CascadeClassifier(cascPath)

    cap = cv2.VideoCapture('http://192.168.1.237:8080/?action=stream&ignored.mjpg')
    cap.set(3, 640)
    cap.set(4, 480)

    pan_position = 7
    tilt_position = 6

    evt = threading.Event()

    while True:
        ret, frame = cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        faces = faceCascade.detectMultiScale(
            gray,
            scaleFactor=1.05,
            minNeighbors=10,
            minSize=(30, 30),
            flags=cv2.CASCADE_SCALE_IMAGE
        )

        tracking_num = 1

        if not type(faces) is tuple:
            faces = faces[0:tracking_num]

        else:
            center_x = 320
            center_y = 240


        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            center_x = x + (w / 2)
            center_y = y + (h / 2)
            text = str(center_x) + ", " + str(center_y)
            cv2.putText(frame, text, (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 255), 2)

        cw_flag = False
        ccw_flag = False
        up_flag = False
        down_flag = False

        bias = 0.06

        if not (298 <= center_x <= 352):
            if center_x < 298:
                ccw_flag = True
            elif center_x > 352:
                cw_flag = True

        if not (208 <= center_y <= 272):
            if center_y < 208:
                up_flag = True
            elif center_y > 272:
                down_flag = True

        if cw_flag is True:
            pan_position -= bias
        elif ccw_flag is True:
            pan_position += bias

        if up_flag is True:
            tilt_position -= bias
        elif down_flag is True:
            tilt_position += bias

        if pan_position > 11.5:
            pan_position = 11.5
        elif pan_position < 2.5:
            pan_position = 2.5

        if tilt_position > 7:
            tilt_position = 7
        elif tilt_position < 2.5:
            tilt_position = 2.5

        data = [pan_position, '/', tilt_position]
        q.put((data, evt))
        evt.wait()

        cv2.imshow('Video', frame)

        if cv2.waitKey(1) == 27:
            break

    return 0


if __name__ == '__main__':
    q = Queue()
    network_thread = threading.Thread(target=networking, args=(q, ))
    image_thread = threading.Thread(target=imaging, args=(q, ))
    network_thread.start()
    image_thread.start()

    q.join()
