## Video summarisation using background estimation


### This model uses general CV techniques to estimate the background in the video, and then judge the foreground for any movement, whereever lot of movement is detected, that frame is selected for the summary.
### This kind of model is very useful in generating summaries of long CCTV videos, where instead of watching the whole video footage which is hours long, we can just watch the parts where heavy motion occured.


#### Steps to run:
It contains a jupyter notebook, just open the file and give the path of the video to the first line - 
*cap = cv2.VideoCapture('VIDEO_PATH_HERE')*
and your output will be in a file called filename.mp4 in the same directory.

## One of the generated summary
![Alt Text](https://github.com/Dsdroid1/Video-Summarizer/blob/main/background-estimation/filename.gif)
