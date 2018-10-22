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

add_desc(test_array,'holi','metal')





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


