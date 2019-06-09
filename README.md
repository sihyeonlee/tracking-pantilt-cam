## tracking-pantilt-cam
Raspberry Pi Camera로 얼굴을 감지하여, pantilt 방식으로 고정한 서보모터 제어로 Pi Camera가 얼굴을 추적하는 것을 목표로 합니다.

### Implementation method
1. Pi Camera로 촬영되는 이미지를 mjpg-streamer를 이용하여 실시간 스트리밍
2. 데스크탑에서 opencv를 이용하여 스트리밍 영상 캡쳐 후, 얼굴 감지 (Haarcascade 사용)
3. 화면 중앙 10% 마진 내에 얼굴을 위치시키기 위해서, 일정 영역 외에서 감지되면, UDP 통신으로 라즈베리파이에 Pan Tilt Position 전송
4. 받은 Position 값을 이용하여 라즈베리파이에서 서보 모터 제어

### Environment
* Raspberry Pi 3
    * HW
        * MG946R Servo Motor * 2
        * Pi Camera V2.1
    * SW
        * mjpg-streamer

* Desktop
    * OpenCV 4.1

### Note
* 라즈베리파이에서 PWM 제어시 소프트웨어로 구현된 PWM이라 떨림 문제 생겨서 추후 하드웨어 방식의 PWM으로 구현 필요.
* 얼굴 인식률 현저히 저하 -> Haarcascade외에 다른 방식으로 구현 필요
* 라즈베리파이 성능으로 동시에 얼굴 감지 및 서보모터 제어하기에 역부족

### After-Plan
* 얼굴 인식이 아닌 object-tracking으로 시도 하기.
* ML로 개인 얼굴 인식률 강화하기.

### Log
* 2019-06-05
    * mjpg-streamer 설치 및 opencv 4.1에서 http를 통하여 mjpg를 읽어와 얼굴 감지
* 2019-06-07
    * Raspberrypi 3 및 Camera, Servo 부품 설계 및 프린팅
* 2019-06-09
    * 1차 Face Tracking 완료