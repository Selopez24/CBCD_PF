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
import match_functions as match
import librosa
from psycopg2.extensions import register_adapter, AsIs


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

def add_data(descriptors, filename, genre, data, fs): # Function to fill db from any file
    
    conn = psycopg2.connect(database=DBNAME)
    cur = conn.cursor()



    
    cur.execute('INSERT INTO audio_files(filename, genre, descriptors, data, fs) VALUES (%s, %s, %s, %s, %s);' , (filename, genre, descriptors.tolist(), data.tolist(), fs))
    
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
            
            data, fs = match.spectrogram_gen(filename, '0')        # file_name // fig_id
    
    
            
            img_db = cv2.imread('../figures/fig_%s.png' % ('0'), cv2.IMREAD_GRAYSCALE)
            
            
            
            
            # find the keypoints and descriptors with ORB
            kp_db, des_db = orb.detectAndCompute(img_db, None)
            
            
            
            add_data(des_db, filename, genre, data, fs) #Fills the database 

            
           
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

def get_candidate_fs(filename): #Query to get individual name based on id
    conn = psycopg2.connect(database=DBNAME)
    cur = conn.cursor()
    
    
    
    cur.execute('SELECT fs FROM audio_files WHERE filename = (%s);', (filename,))
    
    candidate_fs = cur.fetchall()
    
    
    print('>>>Get from DB')
    
    
    
    
    cur.close()
    conn.commit()
    conn.close()
    
    return candidate_fs

def get_candidate_data(filename): #Query to get individual name based on id
    conn = psycopg2.connect(database=DBNAME)
    cur = conn.cursor()
    
    
    
    cur.execute('SELECT data FROM audio_files WHERE filename = (%s);', (filename,))
    
    candidate_data = cur.fetchall()
    
    
    print('>>>Get from DB')
    
    
    
    
    cur.close()
    conn.commit()
    conn.close()
    
    return candidate_data

def get_names(candidates_id): #Function to get all candidates filenames based on id
    names = np.array([])
    for i in range(len(candidates_id)):
        names = np.append(names,get_candidate_name(candidates_id[i]))

    #print(names)
    return names

def get_fs(filename): #Function to get all candidates filenames based on id
    fs = np.array([])
    fs = get_candidate_fs(filename)

    fs = np.append(fs,0)

    fs = np.delete(fs,len(fs)-1)


    #print(names)
    return fs

def get_data(filename): #Function to get all candidates filenames based on id
    data = np.array([])
    data = get_candidate_data(filename)
  
    data = np.append(data,0 )
    
    data = np.delete(data,len(data)-1)

    #print(names)
    return data