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


## We have made several models for our application which is video summarisation:

+ **Trivial Video Summarisation:**  
The video frames are analysed one by one and difference between the frames (in terms of color composition and spatial distance in the color space) is calculated, frame pairs with extreme values of these factors are then selected in the hope that they would either belong to start or end of individual scenes of a video and collated into one summary video.

+ **Generating summary on subtitles:**  
The input program tries to extract the subtitles from the audio sample attached with the video and then uses Natural Language Processing to determine important time stamps in subtitles, and consequently audio to generate list of important blocks which are then coalesced into a single summarised video. A prototype was also created using django framework.

+ **Generating summary based o **
