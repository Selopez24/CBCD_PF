#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 16 09:35:52 2018

@author: sebastian
"""

# Database code testing for storing descriptors from original sampels.

import psycopg2
import numpy as np

test_array = np.array([[1, 2,5], [3, 4,6],[5,6,7]])

DBNAME = 'sebastian'



def update_desc(descriptors, audio_id):
    
    conn = psycopg2.connect(database=DBNAME)
    cur = conn.cursor()
    
    cur.execute('UPDATE audio_files SET descriptors = %s WHERE audio_id = %s;', (descriptors.tolist(), audio_id))
    
    print('>>>Update')
    
    
    
    cur.close()
    conn.commit()
    conn.close()
    

    

def add_desc(descriptors, filename, genre):
    
    conn = psycopg2.connect(database=DBNAME)
    cur = conn.cursor()
    
    cur.execute('INSERT INTO audio_files(filename, genre, descriptors) VALUES (%s, %s, %s);' , (filename, genre, descriptors.tolist()))
    
    print('>>>Add')
    
    
    
    cur.close()
    conn.commit()
    conn.close()
    

def get_desc():
    
    conn = psycopg2.connect(database=DBNAME)
    cur = conn.cursor()
    
    cur.execute('SELECT descriptors FROM audio_files;')
    
    desc_db = cur.fecthall()
    
    print('>>>Get')
    
    print(desc_db)
    
    
    
    cur.close()
    conn.commit()
    conn.close()



def get_candidate_name(candidates_id): #Query to get individual name based on id
    conn = psycopg2.connect(database=DBNAME)
    cur = conn.cursor()
    
    
    
    cur.execute('SELECT filename FROM audio_files WHERE audio_id = (%s);', (candidates_id,))
    
    candidate_name = cur.fetchall()
    
    
    print('>>>Get from DB')
    
    
    
    
    cur.close()
    conn.commit()
    conn.close()
    
    return candidate_name

def get_names(): #Function to get all candidates filenames
    names = np.array([])
    for i in range(len(candidates_id)):
        names = np.append(names,get_candidate_name(candidates_id[i]))
    
    return names


#def add_desc(content):
#  """Add a post to the 'database' with the current timestamp."""
#  db = psycopg2.connect(database=DBNAME)
#  c = db.cursor()
#  c.execute("insert into posts values (%s)", (bleach.clean(content),))  # good
#  db.commit()
#  db.close()
#
#def get_desc():
#  """Return all posts from the 'database', most recent first."""
#  db = psycopg2.connect(database=DBNAME)
#  c = db.cursor()
#  c.execute("select content, time from posts order by time desc")
#  posts = c.fetchall()
#  db.close()
#  return posts


