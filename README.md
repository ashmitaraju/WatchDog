# Welcome to WatchDog!

**WatchDog** is a smart surveillance system that leverages the power of computer vision and cloud computing technology to automatically scan video streams or frames from Closed-circuit television (CCTV) or Web cameras to detected intruders and unauthorized individuals and alert immediately to take appropriate action.

[Try it out yourself!](https://watchdogsok.azurewebsites.net/)


## FaceAPI
WatchDog makes use of the Azure Face API to train and recognize the faces of trusted individuals and to simultaneously alert appropriately if an unknown individual, (potentially maliciously) is encountered.

## Activity Tracking
A multi-camera setup is proposed to  track the movements and activities of each person in the closed circuit, and allow for better assessment of his/her work.

## Raspberry Pi Surveillance Devices
Raspberry Pi 3s fitted with Cameras are used for surveillance. The Pis are programmed to constantly scan the video stream from the cameras and detect human faces in the video using OpenCV. The detected faces are then identified using Microsoft Azure's Face API to determine if they are trusted individuals or trespassers.

### Motivation
This project was created by a team of students from R V College of Engineering, as a part of Microsoft Academia Accelerator Program's contest, code.fun.do.

### Instructions
1. Clone the repository 
2. Install the requirements specified in requirements.txt
3. Place the [config](https://1drv.ms/u/s!AuPyeSIGdEA3gygMFeZu3PDK2XCg) file in the root directory
4. Sign up on the [website](https://watchdogsok.azurewebsites.net/) and train the API with authorized faces. (If the website throws an Internal Server Error, please reload the page). 
5. Run ```videoAnalyser.py <username>```. Username is sys.argv[1] and should be the same as the one entered during SignUp.
6. This script will open the webcam which will emulate the CCTV cameras. 
