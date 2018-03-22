# Welcome to WatchDog!

**WatchDog** is a smart surveillance system that leverages the power of computer vision and cloud computing technology to automatically scan video streams or frames from Closed-circuit television (CCTV) or Web cameras to detected intruders and unauthorized individuals and alert immediately to take appropriate action.

[Try it out yourself!](http://watchdogsok.pythonanywhere.com/)

## Motion Detection 

A local motion detection module has been implemented. This prevents unwanted calls to APIs when there is no motion detected. 

## Face Detection 

If there is some motion detected, a local face detector is run on the frames. If a face is detected, the cropped image of the frame is sent to the Azure Face API to determine if the face is authorized or not. 

## FaceAPI
WatchDog makes use of the Azure Face API to train and recognize the faces of trusted individuals. When faces of trusted individuals are encountered, no action is taken. If it comes across an unrecognized face, it saved in the database with the timestamp and also the location of the camera.  

### Multiple Cameras 

If there are multiple cameras set up for a particular account, they can be tracked separately on the website, under the tab Security Breaches. 


## Raspberry Pi Surveillance Devices
Raspberry Pi 3s fitted with Cameras are used for surveillance. The Pis are programmed to constantly scan the video stream from the cameras and detect motion and human faces in the video using OpenCV. The detected faces are then identified using Microsoft Azure's Face API to determine if they are trusted individuals or trespassers.

### Motivation
This project was created by a team of students from R V College of Engineering, as a part of Microsoft Academia Accelerator Program's contest, code.fun.do.

### Instructions
1. Clone the repository 
2. Install the requirements specified in requirements.txt. (pip install -r requirements.txt)
3. Sign up on the [website](http://watchdogsok.pythonanywhere.com/) and train the API with authorized faces. (If the website throws an Internal Server Error, please reload the page). 
4. Run videoAnalyse.py <username>. Username is sys.argv[1] and should be the same as the one entered during SignUp.
5. This script will open the webcam which will emulate the CCTV cameras.
6. If an authorised face is detected, it will be displayed on the console.
7. Unauthorized faces can be viewed on the website under security breaches.
