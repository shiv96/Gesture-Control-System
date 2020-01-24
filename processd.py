# -*- coding: utf-8 -*-
"""
Created on Fri Aug 31 23:16:20 2018

@author: SHIV
"""

import psutil


VLC = "vlc.exe"
CHROME = "chrome.exe"
MUSIC= "Music.UI.exe"
GAME = "Highway Racer.exe"



def current_process():
    count=0
    for proc in psutil.process_iter():

        if proc.name()==VLC:
            return "vlc"

        if proc.name()==MUSIC:
            return "music"
            
        if proc.name()==CHROME:
            return "chrome"
        
        if proc.name()==GAME:
            return "game"
            
                

current_process()            
            
            
    
            
   
    
        
       
