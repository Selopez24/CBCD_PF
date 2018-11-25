from scipy import signal
import matplotlib.pyplot as plt
from scipy.io import wavfile
import descdb as db
import glob
import cv2
import numpy as np
import librosa



# Set up BFMatcher

bf = cv2.BFMatcher_create(cv2.NORM_HAMMING, crossCheck=False)
bf.clear() # clears the 'bag of features' 
# Initiate ORB detector

orb = cv2.ORB_create()





def spectrogram_gen (audio_file, fig_id): #Generates spectrogram to fingerprint an audio file
    
    #Reading song
    data, fs = librosa.load(audio_file)
    
    #Hanning window, 8192 points and 0.75 overlap as in [22]
    f, t, Sxx = signal.spectrogram(data, fs, window=('hann'),nperseg=8192 ,noverlap=0.75) 
    plt.pcolormesh(t, f, Sxx)
    plt.ylim(top=650)  # adjust the top leaving bottom unchanged
    plt.ylim(bottom=20)
    plt.ylabel('Frequency [Hz]', fontsize = 18)
    plt.xlabel('Time [sec]',fontsize = 18)
    #plt.title(audio_file, fontsize = 18)
    #plt.axis('off')
    plt.savefig('../figures/fig_%s.png' % (fig_id), bbox_inches= 'tight')
    
    return data, fs


# Function to train the system with local files based on folders structure and filenames used
genre = 'metal' # Genre to read 
dataset = '../dataset.wav/%s.wav/*.wav' % (genre) #dataset path = ../dataset.wav/'genre'.wav/*.wav

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
        

def get_candidates_id(desc_q): # function to get candidates id based on the order they are in DB (order in BF 'bag')
                               #desc_q = descrptors of query sample
    
    matches = bf.match(desc_q)
    matches = sorted(matches, key = lambda x:x.distance)
        
    matches_id_array = np.array([])
    matches_distance_array = np.array([])
    
    #Indexing
    for i in range(len(matches)):
        matches_id_array= np.append(matches_id_array,[matches[i].imgIdx]) 
        matches_distance_array=np.append(matches_distance_array,[matches[i].distance]) 
        #print (matches[i].imgIdx)
        #print (matches[i].distance)
    
    
    #Finding files id corresponding to the matches, based on the mean of cumulative frequencies of all matched descriptor
    unique_elements, counts_elements = np.unique(matches_id_array, return_counts=True)
    
    candidates_index= np.where(counts_elements>counts_elements.mean())
    candidates_id = np.array([])
    
    for i in range(len(candidates_index[0])):
        candidates_id = np.append(candidates_id, unique_elements[candidates_index[0][i]])
        
    #print(candidates_id) # id of candidates based on the index of BFmatcher
    
    return candidates_id