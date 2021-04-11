import numpy as np
import cv2 as cv2

k = 10

cap = cv2.VideoCapture('corona.mp4')
frame_width = int(cap.get(3))
frame_height = int(cap.get(4))
size = (frame_width, frame_height)

i = 0
img_array = []
while cap.isOpened():
    ret, frame = cap.read()

    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break

    img_array.append(frame)

cap.release()

print('while worked and image array is created')

print(len(img_array))

j = 0
out_imgs = []

while j in range(len(img_array)):
    index = np.random.choice(range(j, j + k))
    out_imgs.append(img_array[index])
    j += k

out = cv2.VideoWriter('summary.avi', cv2.VideoWriter_fourcc(*'MJPG'), 15, size)

for k in range(len(out_imgs)):
    out.write(out_imgs[k])

out.release()
print('video is formed')

print('trying to play video')
cap2= cv2.VideoCapture('summary.avi')

while cap2.isOpened():
    ret, frame2 = cap.read()
    if not ret:
        print('summary vid cant be played')
        break
    cv2.imshow('summary', frame2)
    if cv2.waitKey(1) == ord('q'):
        break

cap2.release()

cv2.destroyAllWindows()



