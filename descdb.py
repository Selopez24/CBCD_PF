#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 16 09:35:52 2018

@author: sebastian
"""

import psycopg2
from scipy import signal
import matplotlib.pyplot as plt
from scipy.io import wavfile
import descdb as db
import glob
import cv2
import numpy as np
from match_functions import spectrogram_gen


DBNAME = 'sebastian'  ## DB according to user or service


# Set up BFMatcher

bf = cv2.BFMatcher_create(cv2.NORM_HAMMING, crossCheck=False)
bf.clear() # clears the 'bag of features' 
# Initiate ORB detector

orb = cv2.ORB_create()



def update_desc(descriptors, audio_id): ## function to update descriptors or any row of DB table changing parameters
    
    conn = psycopg2.connect(database=DBNAME)
    cur = conn.cursor()
    
    cur.execute('UPDATE audio_files SET descriptors = %s WHERE audio_id = %s;', (descriptors.tolist(), audio_id)) # Also change parameters here
    
    print('>>>Update in DB')
    
    
    
    cur.close()
    conn.commit()
    conn.close()

def add_data(descriptors, filename, genre): # Function to fill db from any data
    
    conn = psycopg2.connect(database=DBNAME)
    cur = conn.cursor()
    
    cur.execute('INSERT INTO audio_files(filename, genre, descriptors) VALUES (%s, %s, %s);' , (filename, genre, descriptors.tolist()))
    
    print('>>>Add to DB')
    
    
    
    cur.close()
    conn.commit()
    conn.close()
    
    
def get_desc(): #Query to get descriptors
    
    conn = psycopg2.connect(database=DBNAME)
    cur = conn.cursor()
    
    cur.execute('SELECT descriptors FROM audio_files;')
    
    desc_db = cur.fetchall()
    
    print('>>>Get from DB')
    
    
    
    
    cur.close()
    conn.commit()
    conn.close()
    
    return desc_db


#Function to fill the DB from local files based on folder structure and filenames used
genre = 'metal' # Genre to read 
dataset = '../dataset.wav/%s.wav/*.wav' % (genre) #dataset path = ../dataset.wav/'genre'.wav/*.wav

def data2db(dataset, genre, min_file_number, max_file_number):
    for filename in glob.iglob(dataset):  #Read every .wav file in directory 
    
        if min_file_number<max_file_number   : 
        
            filename = "../dataset.wav/%s.wav/%s%d.wav" % (genre, genre, min_file_number) 
            
            spectrogram_gen(filename, '0')        # file_name // fig_id
    
    
            
            img_db = cv2.imread('../figures/fig_%s.png' % ('0'), cv2.IMREAD_GRAYSCALE)
            
            
            
            
            # find the keypoints and descriptors with ORB
            kp_db, des_db = orb.detectAndCompute(img_db, None)
            
            
            
            add_data(des_db, filename, genre) #Fills the database 

            
           
            min_file_number+=1
            print(filename)


def get_candidate_name(candidate_id): #Query to get individual name based on id
    conn = psycopg2.connect(database=DBNAME)
    cur = conn.cursor()
    
    
    
    cur.execute('SELECT filename FROM audio_files WHERE audio_id = (%s);', (candidate_id,))
    
    candidate_name = cur.fetchall()
    
    
    print('>>>Get from DB')
    
    
    
    
    cur.close()
    conn.commit()
    conn.close()
    
    return candidate_name

def get_names(candidates_id): #Function to get all candidates filenames based on id
    names = np.array([])
    for i in range(len(candidates_id)):
        names = np.append(names,get_candidate_name(candidates_id[i]))
    print(names)
    return names