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