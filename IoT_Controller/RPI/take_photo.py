import cv2

cap = cv2.VideoCapture(0) # 노트북 웹캠을 카메라로 사용
width = 1024
height = 768

cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

ret, frame = cap.read() # 사진 촬영
frame = cv2.flip(frame, 1) # 좌우 대칭
frame = cv2.resize(frame, (width, height))

# 파일이름 형식 설정
cv2.imwrite('test.jpg', frame) # 사진 저장

cap.release()
cv2.destroyAllWindows()