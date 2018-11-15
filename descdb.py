#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 16 09:35:52 2018

@author: sebastian
"""

import psycopg2


DBNAME = 'sebastian'


def update_desc(descriptors, audio_id):
    
    conn = psycopg2.connect(database=DBNAME)
    cur = conn.cursor()
    
    cur.execute('UPDATE audio_files SET descriptors = %s WHERE audio_id = %s;', (descriptors.tolist(), audio_id))
    
    print('>>>Updat in DB')
    
    
    
    cur.close()
    conn.commit()
    conn.close()

def add_desc(descriptors, filename, genre):
    
    conn = psycopg2.connect(database=DBNAME)
    cur = conn.cursor()
    
    cur.execute('INSERT INTO audio_files(filename, genre, descriptors) VALUES (%s, %s, %s);' , (filename, genre, descriptors.tolist()))
    
    print('>>>Add to DB')
    
    
    
    cur.close()
    conn.commit()
    conn.close()
    
    
def get_desc():
    
    conn = psycopg2.connect(database=DBNAME)
    cur = conn.cursor()
    
    cur.execute('SELECT descriptors FROM audio_files;')
    
    desc_db = cur.fetchall()
    
    print('>>>Get from DB')
    
    
    
    
    cur.close()
    conn.commit()
    conn.close()
    
    return desc_db

def get_candidates(candidate_id):
    conn = psycopg2.connect(database=DBNAME)
    cur = conn.cursor()
    
    cur.execute('SELECT filename FROM audio_files WHERE audio_id = (%s);', (candidate_id))
    
    desc_db = cur.fetchall()
    
    print('>>>Get from DB')
    
    
    
    
    cur.close()
    conn.commit()
    conn.close()
    
    return desc_db

