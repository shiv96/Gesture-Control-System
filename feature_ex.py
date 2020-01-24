# -*- coding: utf-8 -*-
"""
Created on Fri Aug 10 23:13:01 2018

@author: lenovo
"""

import cv2
import numpy as np
from collections import deque
from processd import current_process
import pyautogui as gui
import time



buff=128
oldx=0
oldy=0
currx=0
curry=0
counter=0
counter1=0
call_counter=0;
flag=0
last_motion=""
flag_do_gesture=0
current_gesture = []

yellow_lower = np.array([7, 96, 85])                          # HSV yellow lower
yellow_upper = np.array([255, 255, 255])    

blue_lower = np.array([110,50,50])
blue_upper = np.array([130,255,255])




cap = cv2.VideoCapture(0)



def perform(gesture):
    current=current_process()
    
    if(current=="chrome"):
        
        if(gesture=="N"):
            gui.hotkey('DOWN')
            gui.hotkey('DOWN')
            gui.hotkey('DOWN')
            gui.hotkey('DOWN')
            gui.hotkey('DOWN')
                
        if(gesture=="S"):
            gui.hotkey('UP')
            gui.hotkey('UP')
            gui.hotkey('UP')
            gui.hotkey('UP')
            gui.hotkey('UP')

        if(gesture=="E"):
            gui.hotkey('LEFT')
            gui.hotkey('LEFT')
            gui.hotkey('LEFT')

        if(gesture=="W"):
            gui.hotkey('RIGHT')
            gui.hotkey('RIGHT')
            gui.hotkey('RIGHT')

        #if(gesture=="NW"):
            #gui.hotkey('ctrl','t')

        if(gesture=="SW"):
            gui.hotkey('ctrl','-')

        if(gesture=="NE"):
            gui.hotkey('ctrl','+')

        if(gesture=="SE"):
            gui.hotkey('alt','f4')
        
            
    if(current=="vlc"):
        if(gesture=="S"):
            gui.hotkey('DOWN')

        if(gesture=="N"):
            gui.hotkey('UP')

        if(gesture=="E"):
            gui.hotkey('RIGHT')

        if(gesture=="W"):
            gui.hotkey('LEFT')

        if(gesture=="SW"):
            gui.hotkey('space')

        if(gesture=="SE"):
            print("SE")
            gui.hotkey('alt','f4')


    if(current=="music"):
        if(gesture=="S"):
            gui.hotkey('volumedown')

        if(gesture=="N"):
            gui.hotkey('volumeup')

        if(gesture=="SW"):
            gui.hotkey('space')

        if(gesture=="SE"):
            gui.hotkey('alt','f4')
            
           
    if(current=="game"):
       
         print("game")
         if(gesture=="S"):
             #gui.keyUp('LEFT')
             #gui.keyUp('RIGHT') 
             #gui.keyUp('UP')
             
             gui.keyDown('DOWN')
            # gui.keyUp('DOWN')
             
             """
             counter1=20
             while(counter1>0):
                 gui.hotkey('DOWN')
                 counter1=counter1-1 
                 """
        
         if(gesture=="N"):
            
            #gui.keyUp('LEFT')
            #gui.keyUp('RIGHT')
            #gui.keyUp('DOWN')
            
            gui.keyDown('UP')
            
            """
            counter1=20
            while(counter1>0):
                gui.hotkey('UP')
                counter1=counter1-1 
                """
                
         if(gesture=="E"):
             
            #gui.keyUp('LEFT')
            #gui.keyUp('RIGHT')
            #gui.keyUp('DOWN')
            
            gui.keyDown('RIGHT')
            """
            counter1=30
            gui.keyDown('RIGHT')
            while(counter1>0):
                counter1=counter1-1
            gui.keyUp('RIGHT')
            """
                
         if(gesture=="W"):
            
            #gui.keyUp('UP')
            #gui.keyUp('DOWN')
            #gui.keyUp('RIGHT')

            gui.keyDown('LEFT')
            """
            counter1=30
            gui.keyDown('LEFT')
            while(counter1>0):
                counter1=counter1-1
            gui.keyUp('LEFT')
            """
                
            
            
        
    
    


while(1):

    
    # Take each frame
    _, frame = cap.read()
    
    #for not touching frame
    img=frame
    img = cv2.flip(img, 1)
    img = cv2.resize(img, (480, 360))
    #this part is over

    # Convert BGR to HSV
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # define range of blue color in HSV


    # Threshold the HSV image to get only blue colors
    mask = cv2.inRange(hsv, blue_lower, blue_upper)
    
    blur = cv2.medianBlur(mask, 15)
    blur = cv2.GaussianBlur(blur , (5,5), 0)
    temp,thresh = cv2.threshold(blur,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    
    _,thresh = cv2.threshold(blur,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    cv2.imshow("Thresh", thresh)

    _, contours, _ = cv2.findContours(thresh.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    
    print(len(contours))
    
    
    
    if(len(contours)==0):
        line_pts = deque(maxlen = buff)
        print("Empty Image")
       
        """processed_gesture_hand1 = tuple(process_gesture(current_gesture))
        
        if flag_do_gesture == 0:                                            # flag_do_gesture to make sure that gesture runs only once and not repeatedly
            if processed_gesture_hand1 != ():
                do_gesture_action(processed_gesture_hand1)
            flag_do_gesture = 1
        print(processed_gesture_hand1)     """                                 # for debugging purposes
        created_gesture = []
        flag = True

    else:
        flag_do_gesture = 0
        #max_contour = max(contours, key = cv2.contourArea)
        
        area_t=0;
        thresh_area=2000;
        for i in contours:
            temp=cv2.contourArea(i)
            print("inside: ",temp)
            if(temp>area_t and temp<thresh_area):
                area_t=temp
                max_contour=i
            
        
        rect1 = cv2.minAreaRect(max_contour)
        (w, h) = rect1[1]
        area_c = w*h
        print("area:",area_c)

        box = cv2.boxPoints(rect1)
        box = np.int0(box)
        
        
        
        if(area_t>350):
            print("suff area:",area_c)
            
            center=list(rect1[0])
            currx=int(center[0])
            curry=int(center[1])
            print("last_motion:",last_motion)
            print("curr pos: ",currx,curry)
            cv2.drawContours(img,[box],0,(0,0,255),2)
            cv2.circle(img, (currx, curry), 2, (0, 255, 0), 2)
            
            
            
            
            if(counter==0):
                oldx=currx
                oldy=curry


                
            call_counter=call_counter+1
            counter=counter+1
            
            diffx, diffy=0, 0
            if counter>5:
                diffx=currx-oldx
                diffy=curry-oldy
                counter=0

                
            print("Differences: ",diffx,diffy)   
            
            if(diffx<40 and diffy<40):
                
            
                if(diffx>15 and abs(diffy)<15):
                    last_motion="E"
                    perform(last_motion);
                    current_gesture.append(last_motion)
                    
                elif(diffx<-15 and abs(diffy)<15):
                    last_motion="W"
                    perform(last_motion);
                    current_gesture.append(last_motion)
                    
                elif(abs(diffx)<15 and diffy<-15 ):
                    last_motion="N"
                    perform(last_motion);
                    current_gesture.append(last_motion)
                   
                elif(abs(diffx)<15 and diffy>15):
                    last_motion="S"
                    perform(last_motion);
                    current_gesture.append(last_motion)
     
                    
                elif diffx > 20 and diffy > 20:
                    last_motion="SE"
                    perform(last_motion);
                    current_gesture.append(last_motion)
                        
                elif diffx < -20 and diffy > 20:
                    last_motion="SW"
                    perform(last_motion);
                    current_gesture.append(last_motion)
                    
                elif diffx > 20 and diffy < -20:
                    last_motion="NE"
                    perform(last_motion);
                    current_gesture.append(last_motion)
                    
                elif diffx < -20 and diffy < -20:
                    last_motion="NW"
                    perform(last_motion);
                    current_gesture.append(last_motion)
                    
                
                    
                
                
            flag=False
            
        
    cv2.imshow("Detected: ", img)    
    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break

cv2.destroyAllWindows()
