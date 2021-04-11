# Video-Summarizer

## SWLab4 Mini-Project for Winter 21

### Contributors:-
* [Kartik Kshirsagar (BT18CSE011)](https://github.com/kartikkshirsagar)
* [Kunal Moharkar (BT18CSE018)](https://github.com/KunalMoharkar)
* [Dhruv Sharma (BT18CSE046)](https://github.com/dsdroid1)
* [Nitin Wartkar (BT18CSE051)](https://github.com/nitinosiris)
* [Chinmay Hattewar (BT18CSE055)](https://github.com/chinuh037)
* [Rishu Kumar (BT18CSE060)](https://github.com/dsdroid1)
* [Karan Motghare (BT18CSE061)](https://github.com/karanmotghare)
* [Suhrid Mulay (BT18CSE078)](https://github.com/suhridmulay)
* [Aryan Patil (BT18CSE096)](https://github.com/aryanpatil)
* [Ninad Dadmal (BT18CSE137)](https://github.com/Ninad10code)


## The following models showcase different methodologies to demonstrate Video Summarisation:
+ **Models based on observations and statistics (conditional models,do not generalize well,just as a basic attempt)**
  + `Random Frame from N-Frame window` 
  + `K-frames from a N-frame window`

+ **Models based on simple CV features**
  + `Image Histogram as a Feature over N frames`
  + `Video summarisation using Histogram and Spatial Distance measurement`
  + `Video summarisation using Background estimation technique`

+ **Models based on Machine Learning techniques**
  + `Audio/Subtitle based (Different from considering just images)`


---------------------------------------------------------------------------------------------------------------------------------------------------------------------------

## We have made several models for our application which is video summarisation:
+ **Models based on observations and statistics (conditional models,do not generalize well,just as a basic attempt)**
+ `Random Frame from N-Frame window` :
In this simple model, we take a window size of N frames, and randomly choose 1 frame to keep in the summary. This is a very basic estimate to create a summary. This assumes that the whole video is consisting of important events spanning over multiple frame(Preferrably >N), and selecting any one of those captures the essence of that event. Of course, this is an entirely situational model, but is helpful in downsizing the video in time dimension without changing its meaning much(with lower N values). Major Use Case: From a lecture,generate a summary of major ppt slides(short summary to know which topics were covered when by manually viewing it)

+ `K-frames from a N-frame window` :
This is an extension of the earlier model. In this we increase the N value to be much larger,and then select a stream of K frames from that N. This assumes that an important event cannot be captured by a single frame, rather a stream of frames is more appropriate. This is totally valid as we will see that this observation gives rise to the major logic of other methods. Here the frames are still selected randomly, which as we can estimate will not be optimal(Optimality decreases as video size increases).

Thus, instead of randomly selecting few frames,we move on to much complex models,which compute a descriptor for a fream/sequence of frames and use that descriptor to evaluate whether the frame is good or not.

+ **Models based on simple CV features**
+ `Image Histogram as a Feature over N frames` :
Now, to select frames, we compute a descriptor based on the properties of the image(over time). A basic feature that comes to mind is the histogram of the image, which as we are aware, is also used to fetch similar images from an image query database(one of the methods is by comparing the histograms). Thus, we extend this idea to videos,claiming that if some sudden change appears in the image,then the histogram would significantly change. Hence we compute the correlation between 2 histograms, if similar then the image is probably similar to the earlier picked image,and hence need not be picked again. This is of course another primitive model, that is it is only suited well for videos with sudden changes to be summarized. To make it less computationally expensive,we average the image over N frames and then calculate the histogram,sacrificing accuracy over time. This has a threshold parameter for similarity,which has to be manually tweaked.

+ `Feature Vector(Convolutional part of an NN) Encoding of an images as a feature` :
+ `Video summarisation using Histogram and Spatial Distance measurement` :  
Image features can be understood in two domains, a frequency domain, which can be accessed via the histogram, and a spatial domain which can be accesed via the raw bitmap of the frame. We use euclidean and cosine distance between pairs of frames to locate drastic changes in scene (either in spatial or frequency domain). These frames are then selected and colaesced into a summary video. This method works extremely well for presentations style videos which can be highly compressed into a selection of as lows as 3% of frames with minimal loss.

Uptil now, all models were either statistical or based on CV features and had some degree of manual setting to get best results.However , we turn to Machine Learnig in order to remove this human dependency
+ `ML based models`
+ `LSTM Based`
+ `Audio/Subtitle based (Different from considering just images)`
+ `GAN based unsupervised learning`

+ **Generating summary on subtitles:**  
The input program tries to extract the subtitles from the audio sample attached with the video and then uses Natural Language Processing to determine important time stamps in subtitles and consequently audio to generate list of important blocks which are then coalesced into a single summarised video
+ **Generating summary based output**
+ ![summarized example](https://github.com/Dsdroid1/Video-Summarizer/tree/main/videoGifs/1.gif)
+ <img src='https://github.com/Dsdroid1/Video-Summarizer/tree/main/videoGifs/1.gif'/>
