#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 24 18:10:17 2018

@author: sebastian
"""
from pydub import AudioSegment
import glob

min_file_number = 0
max_file_number= 100
dist_type = '_+bass_echo'



while min_file_number<max_file_number:
    
    for filename in glob.iglob('../dataset.dist/metal%d.wav' % (min_file_number)):
        if min_file_number<max_file_number:
            
            name= "../dataset.wav/metal.wav/metal%d%s.wav" % (min_file_number, dist_type)       
           
            
            
            sound = AudioSegment.from_file(filename, format="wav")
            
            # sample export
            file_handle = sound.export(name, format="wav")
            
               
            print(filename)
            print (name)
    

    min_file_number+=1
   