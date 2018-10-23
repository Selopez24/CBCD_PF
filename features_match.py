import cv2
import numpy as np
from time import time
from spectrogram import spectrogram_gen
import glob
import descdb as db


#Parameters edfinition

min_file_number = 0 #Sample min index
max_file_number = 5 #Sample max index
genre = 'metal' # Genre to read 
dataset = '../dataset.wav/%s.wav/*.wav' % (genre)



#-----------------------------------------------------------------------------------------------


time0 = time()
# Brute Force Matching and add cluster of training
bf = cv2.BFMatcher_create(cv2.NORM_HAMMING, crossCheck=False)
bf.clear()
# Initiate ORB detector
orb = cv2.ORB_create()

#Function to fill the DB from local files
def data2db(dataset,min_file_number,max_file_number):
    for filename in glob.iglob(dataset):  #Read every .wav file in directory 
    
        if min_file_number<max_file_number   : 
        
            filename = "../dataset.wav/%s.wav/%s%d.wav" % (genre, genre, min_file_number) 
            
            spectrogram_gen(filename, '0')        # file_name // fig_id
    
    
            
            img_db = cv2.imread('../figures/fig_%s.png' % ('0'), cv2.IMREAD_GRAYSCALE)
            
            
            
            
            # find the keypoints and descriptors with ORB
            kp_db, des_db = orb.detectAndCompute(img_db, None)
            
            
            
            db.add_desc(des_db, filename, genre) #Fills the database 

            
           
            min_file_number+=1
            print(filename)
            
            
            
 # Function to train the system with local files           
def train_local(dataset,min_file_number,max_file_number):
    for filename in glob.iglob(dataset):  #Read every .wav file in directory 
    
        if min_file_number<max_file_number   : 
        
            filename = "../dataset.wav/%s.wav/%s%d.wav" % (genre, genre, min_file_number) 
            
            spectrogram_gen(filename, '0')        # file_name // fig_id
    
    
            
            img_db = cv2.imread('../figures/fig_%s.png' % ('0'), cv2.IMREAD_GRAYSCALE)
            
            
            
            
            # find the keypoints and descriptors with ORB
            kp_db, des_db = orb.detectAndCompute(img_db, None)
            
            
            

            clusters = np.array([des_db])
            bf.add(clusters)
           
            min_file_number+=1
            print(filename)
       

# Function to train the system from descriptors in DB
def train_fromdb():
    get_desdb = db.get_desc()
    for descriptor in range(len(get_desdb)):
        des_fromdb= np.asarray(get_desdb[descriptor],  dtype=np.uint8)
        bf.add(des_fromdb)
        
        
        
        


# Audio sample in ====>
        
train_fromdb()


file_ext = '0_+bass_echo'
test_file = "../dataset.wav/%s.wav/%s%s.wav" % (genre, genre, file_ext)
fig_query = 'test'
fig_path = '../figures/fig_%s.png'


spectrogram_gen(test_file, fig_query ) #query file // fig_id
img_q = cv2.imread(fig_path % (fig_query), cv2.IMREAD_GRAYSCALE) # image for kp and desc extratcion 
kp_q, des_q = orb.detectAndCompute(img_q, None) # kp and desc for query image/audio sample



matches = bf.match(des_q)
matches = sorted(matches, key = lambda x:x.distance)

matches_id_array = np.array([])
matches_distance_array = np.array([])

#Indexing
for i in range(len(matches)):
    matches_id_array= np.append(matches_id_array,[matches[i].imgIdx]) 
    matches_distance_array=np.append(matches_distance_array,[matches[i].distance]) 
    print (matches[i].imgIdx)
    #print (matches[i].distance)


unique_elements, counts_elements = np.unique(matches_id_array, return_counts=True)

time1 = time()

print('Execution time = ',time1-time0)








# matches = bf.match(des_q, des_db)



# matching_result = cv2.drawMatches(img_q, kp_q, img_db, kp_db, matches[:25], None, flags=2)

# cv2.imshow("img_q", img_q)
# cv2.imshow("img_db", img_db)
# cv2.imshow("Matching result", matching_result)
# cv2.waitKey(0)
# cv2.destroyAllWindows()