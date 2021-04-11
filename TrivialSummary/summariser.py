"""
VIDEO SUMMARISATION USING FEATURE VECTORS
DEPENDENCIES
*IMPORTANT*
numpy - for array operations
python-opencv - for image/video processing
scipy - for distance calculations

IDEA
1. Extract the feature vector for each frame in a video
2. Wherever the difference between the feature vector is > Threshold, create a new scene
3. Select last 10% of each scene
"""

import numpy as np
import cv2 
from scipy import spatial

filepath = input('Enter path to target video: ') or 'media/videoplayback.mp4'
filename = filepath.split('/')[-1].split('.')[0]

# Load the video
cap = cv2.VideoCapture(filepath)

# Blocks of video
# [FrameNoStart, FrameNoEnd]
blocks = []

# A sentinel vector to compare against
sentinel = np.ones((10, 10)).flatten()

# A sentinel histogram to keep track in histogram space
sentinel_hist = np.ones(shape=(256, 1))

# Output FPS value, it is recommended that it be mantained on low
FPS = 10

# Initialise starting block
curr_block = [0, 0]

# Initialise output writer
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter('{}_summarized.mp4'.format(filename), fourcc, FPS, (640, 360))

# Frame counters
# Processed
fc = 0
# Accepted
afc = 0

while(cap.isOpened()):
    ret, frame = cap.read()

    if ret == False:
        break

    # Every 8 frame
    if fc % 8 != 0:
        fc += 1
        continue

    grayframe = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    ten_by_ten = cv2.resize(grayframe, (10, 10))
    ten_by_ten = np.array(ten_by_ten).flatten()

    curr_frame_hist = cv2.calcHist(grayframe, [0], None, [256], [0, 256])

    # Spatial distance
    spat_dist = spatial.distance.euclidean(ten_by_ten, sentinel)
    # Histogram distance
    hist_dist = spatial.distance.cosine(curr_frame_hist, sentinel_hist) * 1000

    # Accept all extremum values for spatial and histogram distance
    if ((spat_dist < 10 or spat_dist > 600) and (hist_dist < 10 or hist_dist > 700) and (hist_dist > 0.1)):
        print('Scene change detected')
        print('Spatial distance = {}'.format(spat_dist))
        print('Histogram distance = {}'.format(hist_dist))
        if fc - curr_block[0] > 150:
            out.write(frame)
            cv2.imshow('frame', frame)
            afc += 1
        sentinel = ten_by_ten
        sentinel_hist = curr_frame_hist

    fc += 1

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release video file and close windows
cap.release()
cv2.destroyAllWindows()

# Show processing summary
print('Selected {} of {} frames'.format(afc, fc))
print('Summary ration {}'.format(afc / fc))
