#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 26 07:48:27 2018

@author: sebastian
"""

import cv2
import numpy as np
from matplotlib import pyplot as plt
from time import time
import spectrogram
import glob
import psycopg2
import descdb as db


   


# train_img= db // test_img= query
time0 = time()

img_q = cv2.imread('../figures/test.png', cv2.IMREAD_GRAYSCALE) 
img_db = cv2.imread('../figures/test2.png', cv2.IMREAD_GRAYSCALE)
img_test = cv2.imread('../figures/test3.png',cv2.IMREAD_GRAYSCALE)
img_test2 = cv2.imread('../figures/test1.png',cv2.IMREAD_GRAYSCALE)
img_dist = cv2.imread('../figures/test_dist.png',cv2.IMREAD_GRAYSCALE)


# Initiate ORB detector
orb = cv2.ORB_create()

# find the keypoints and descriptors with ORB
kp_q, des_q = orb.detectAndCompute(img_q, None)
kp_db, des_db = orb.detectAndCompute(img_db, None)
kp_test, des_test = orb.detectAndCompute(img_test, None)
kp_test2, des_test2 = orb.detectAndCompute(img_test2, None)
kp_dist, des_dist = orb.detectAndCompute(img_dist, None)


# Brute Force Matching and add cluster of training
bf = cv2.BFMatcher_create(cv2.NORM_HAMMING, crossCheck=False)

bf.clear()

clusters = np.array([des_db])
bf.add(clusters)

clusters2= np.array([des_test])
bf.add(clusters2)

clusters3= np.array([des_q])
bf.add(clusters3)

clusters4= np.array([des_test2])
bf.add(clusters4)

clusters5= np.array([des_dist])
bf.add(clusters5)




#test = db.get_desc()
#test_des = np.asarray(test[0], dtype=np.uint8)
#
#bf.add(test_des)




matches = bf.match(des_dist)
matches = sorted(matches, key = lambda x:x.distance)


#Indexing
for i in range(len(matches)):
    print (matches[i].imgIdx)



time1 = time()

print(time1-time0)

matches = bf.match(des_q, des_db)



#matching_result = cv2.drawMatches(img_q, kp_q, img_db, kp_db, matches[:25], None, flags=2)
#
#cv2.imshow("img_q", img_q)
#cv2.imshow("img_db", img_db)
#cv2.imshow("Matching result", matching_result)
#cv2.waitKey(0)
#cv2.destroyAllWindows()