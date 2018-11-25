#Similarity Algorithm

import sounddevice as sd
import soundfile as wav
from time import time
import numpy as np
import glob as gb
import librosa
import re
import matplotlib.pyplot as plt
import numpy as np
import scipy.signal as signal2
import math
import wave, pylab
import operator
import scipy as sc
import descdb as db
import match_functions as match 

def tryint(s):
    try:
        return int(s)
    except ValueError:
        return s
    
def alphanum_key(s):
    """ Turn a string into a list of string and number chunks.
        "z23a" -> ["z", 23, "a"]
    """
    return [ tryint(c) for c in re.split('([0-9]+)', s) ]
    
def SimilarityChroma(data):
    null=0
    # Load the example clip
    y_data, sr_data = librosa.load(data)
    # Set the hop length; at 22050 Hz, 512 samples ~= 23ms
    hop_length_data = 512
    # Separate harmonics and percussives into two waveforms
    y_harmonic, y_percussive = librosa.effects.hpss(y_data)
    # Beat track on the percussive signal
    tempo, beat_frames = librosa.beat.beat_track(y=y_percussive,sr=sr_data)
    # Compute MFCC features from the raw signal
    mfcc = librosa.feature.mfcc(y=y_data, sr=sr_data, hop_length=hop_length_data, n_mfcc=13)
    # And the first-order differences (delta features)
    mfcc_delta = librosa.feature.delta(mfcc)
    # Stack and synchronize between beat events
    # This time, we'll use the mean value (default) instead of median
    beat_mfcc_delta = librosa.util.sync(np.vstack([mfcc, mfcc_delta]),beat_frames)
    # Compute chroma features from the harmonic signal
    chromagram_data = librosa.feature.chroma_stft(y=y_harmonic,sr=sr_data)
    # Spectrogram 
    f_data, t_data, s_data = sc.signal.spectrogram(y_data, sr_data)
    return (chromagram_data, s_data)

def CorrelationChroma(data1, data2):
    chromagram_data1, s_data1 = SimilarityChroma(data1)
    chromagram_data2, s_data2 = SimilarityChroma(data2)
    #Median Seems to work upside-down
    DCT1 = np.median(sc.fftpack.dct(chromagram_data1,1),1)
    DCT2 = np.median(sc.fftpack.dct(chromagram_data2,1),1)
    #print((Sxx11),(Sxx2),"\n")
    C1 = np.corrcoef(DCT1,DCT2) 
    C1_=(np.abs(1-np.mean(C1)))
    #Median Seems to work upside-down
    SG1 = np.median(sc.fftpack.dct(s_data1,1),1)
    SG2 = np.median(sc.fftpack.dct(s_data2,1),1)
    #print((Sxx11),(Sxx2),"\n")
    C2 = np.corrcoef(SG1,SG2) 
    C2_=(np.abs(1-np.mean(C2)))
    #Mean correlation
    F1=C1_
    F2=C2_
    Features=[F1, F2]
    #print(Features)
    similarity_Chroma=np.amax(Features)
    return(similarity_Chroma, Features)
    
def CorrelationChroma2(data1,data2):
    chromagram_data1, s_data1 = SimilarityChroma(data1)
    chromagram_data2, s_data2 = SimilarityChroma(data2)
    #Median Seems to work upside-down
    DCT1 = np.median(sc.fftpack.dct(chromagram_data1,1),1)
    DCT2 = np.median(sc.fftpack.dct(chromagram_data2,1),1)
    #print((Sxx11),(Sxx2),"\n")
    C1 = np.corrcoef(DCT1,DCT2) 
    C1_=(np.abs(1-np.mean(C1)))
    #Median Seems to work upside-down
    SG1 = np.median(sc.fftpack.dct(s_data1,1),1)
    SG2 = np.median(sc.fftpack.dct(s_data2,1),1)
    #No Var chroma
    NDTC1 = np.var(sc.fftpack.dct(chromagram_data1,1),1)
    NDTC2 = np.var(sc.fftpack.dct(chromagram_data2,1),1)
    F3 = np.abs(1-np.mean(np.corrcoef(NDTC1,NDTC2))) 
    #print((Sxx11),(Sxx2),"\n")
    C2 = np.corrcoef(SG1,SG2) 
    C2_=(np.abs(1-np.mean(C2)))
    #Mean correlation
    F1=C1_
    F2=C2_
    Features=[F1, F2, F3]
    #print(Features)
    similarity_Chroma=np.amax(Features)
    return(similarity_Chroma, Features)

def CorrelationChroma3(data1,data2):
    chromagram_data1, s_data1 = SimilarityChroma(data1)
    chromagram_data2, s_data2 = SimilarityChroma(data2)
    #Median Seems to work upside-down
    DCT1 = np.median(sc.fftpack.dct(chromagram_data1,1),1)
    DCT2 = np.median(sc.fftpack.dct(chromagram_data2,1),1)
    #print((Sxx11),(Sxx2),"\n")
    C1 = np.corrcoef(DCT1,DCT2) 
    C1_=(np.abs(1-np.mean(C1)))
    #Median Seems to work upside-down
    SG1 = np.median(sc.fftpack.dct(s_data1,1),1)
    SG2 = np.median(sc.fftpack.dct(s_data2,1),1)
    #No Mean chroma
    NSG1 = np.mean(sc.fftpack.dct(s_data1,1),1)
    NSG2 = np.mean(sc.fftpack.dct(s_data2,1),1)
    F3 = np.mean(np.corrcoef(NSG1,NSG2)) 
    #print((Sxx11),(Sxx2),"\n")
    C2 = np.corrcoef(SG1,SG2) 
    C2_=(np.abs(1-np.mean(C2)))
    #Mean correlation
    F1=C1_
    F2=C2_
    Features=[F1, F2, F3]
    #print(Features)
    similarity_Chroma=np.amax(Features)
    return(similarity_Chroma, Features)