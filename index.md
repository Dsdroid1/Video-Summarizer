## Video Summarizer
A program that captures and condenses the key moments from a video and summarises it by creating a video which encompassing all the highlights. This is achieved by analysing audio and video to identify key moments which are then marked and cropped and pasted into a single video.

## Team
+ BT18CSE046 - Dhruv Sharma (Leader)<br/>
+ BT18CSE018 - Kunal Moharkar<br/>
+ BT18CSE096 - Aryan Patil<br/>
+ BT18CSE051 - Nitin Wartkar<br/>
+ BT18CSE060 - Rishu Kumar<br/>
+ BT18CSE061 - Karan Motghare<br/>
+ BT18CSE055 - Chinmay Hattewar<br/>
+ BT18CSE078 - Suhrid Mulay<br/>
+ BT18CSE137 - Ninad Dadmal<br/>
+ BT18CSE011 - Kartik Kshirsagar


## Models Created:
+ **Random Frame from N-Frame window**
+ **K-frames from a N-frame window**
+ **N Frame Histogram Summarisation**
+ **Histogram and Spatial distance**
+ **Background estimation technique**
+ **Summarisation using subtitles**


## Implementation Strategy :

*In order to create a basic video summary, we would start by picking out random frames from the video which was performed by the under written model:*

+ **`Random Frame from N-Frame window`** :
In this simple model, we take a window size of N frames, and randomly choose 1 frame to keep in the summary. This is a very basic estimate to create a summary. This assumes that the whole video is consisting of important events spanning over multiple frame(Preferrably >N), and selecting any one of those captures the essence of that event. Of course, this is an entirely situational model, but is helpful in downsizing the video in time dimension without changing its meaning much(with lower N values). Major Use Case: From a lecture,generate a summary of major ppt slides(short summary to know which topics were covered when by manually viewing it)

*Then we moved on to making the summary slightly longer than that was produced by the above model:*

+ **`K-frames from a N-frame window`** :
This is an extension of the earlier model. In this we increase the N value to be much larger,and then select a stream of K frames from that N. This assumes that an important event cannot be captured by a single frame, rather a stream of frames is more appropriate. This is totally valid as we will see that this observation gives rise to the major logic of other methods. Here the frames are still selected randomly, which as we can estimate will not be optimal(Optimality decreases as video size increases).

*Now, instead of randomly selecting few frames, we moved on to much complex models,which compute a descriptor for a fream/sequence of frames and use that descriptor to evaluate whether the frame is good or not. This brings us to implement models using CV techniques*

*So, we thought : Why not compare the histograms of subsequent frames for determining changes in the video? This thought contributed in making of the next model:*

+ **`Image Histogram as a Feature over N frames`** :
Now, to select frames, we compute a descriptor based on the properties of the image(over time). A basic feature that comes to mind is the histogram of the image, which as we are aware, is also used to fetch similar images from an image query database(one of the methods is by comparing the histograms). Thus, we extend this idea to videos,claiming that if some sudden change appears in the image,then the histogram would significantly change. Hence we compute the correlation between 2 histograms, if similar then the image is probably similar to the earlier picked image,and hence need not be picked again. This is of course another primitive model, that is it is only suited well for videos with sudden changes to be summarized. To make it less computationally expensive,we average the image over N frames and then calculate the histogram,sacrificing accuracy over time. This has a threshold parameter for similarity,which has to be manually tweaked.

*Now, we modified the above model so that we would be able to locate drastic changes in the scene using euclidean and cosine distance between the pairs of frames:*

+ **`Video summarisation using Histogram and Spatial Distance measurement`** :  
Image features can be understood in two domains, a frequency domain, which can be accessed via the histogram, and a spatial domain which can be accesed via the raw bitmap of the frame. We use euclidean and cosine distance between pairs of frames to locate drastic changes in scene (either in spatial or frequency domain). These frames are then selected and colaesced into a summary video. This method works extremely well for presentations style videos which can be highly compressed into a selection of as lows as 3% of frames with minimal loss.

  + One of the generated summary:\
    ![Alt Text](./videoGifs/vidsum.gif)

*In certain areas, such as a parking lot, we observed that the movement occurs in the foreground while the background remains static. This thought provoked us in building our next model:*

+ **`Video summarisation using Background estimation technique`** :
This model uses general CV techniques to estimate the background in the video, and then judge the foreground for any movement, whereever lot of movement is detected, that frame is selected for the summary. This kind of model is very useful in generating summaries of long CCTV videos, where instead of watching the whole video footage which is hours long, we can just watch the parts where heavy motion occured.

  + Steps to run:
    It contains a jupyter notebook, just open the file and give the path of the video to the first line<br/> 
    *cap = cv2.VideoCapture('VIDEO_PATH_HERE')*\
    and your output will be in a file called filename.mp4 in the same directory.

  + One of the generated summary:\
    ![Alt Text](./videoGifs/filename.gif)
    

*Until now, all models were either statistical or based on CV features and had some degree of manual setting to get best results.However ,we turn towards Machine Learnig in order to remove this human dependency*

*Given the craze of sports like cricket, football, etc. among youth, it is necessary that we utilise the audio/subtitles in a video to generate a summary much more sensitive towards pointing out important incidents in the game. This brings us to the last model created:*

+ **`Generating summary on subtitles`** :  
The input program tries to extract the subtitles from the audio sample attached with the video and then uses Natural Language Processing to determine important time stamps in subtitles and consequently audio to generate list of important blocks which are then coalesced into a single summarised video
  + One of the generated summary: \
    ![summarized example](./videoGifs/1.gif)
