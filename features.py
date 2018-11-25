import librosa as lb
import librosa.display
import numpy as np
import scipy as sc
import matplotlib.pyplot as plt
import descdb as db

def MelSpectogram(data_name):
    y_data, sr_data = librosa.load(data_name)
    y_harmonic, y_percussive = librosa.effects.hpss(y_data)
    S = librosa.feature.melspectrogram(y_data, sr=44100, n_mels=128)
    log_S = librosa.power_to_db(S, ref=np.max)
    tempo, beats = librosa.beat.beat_track(y=y_percussive, sr=44100, trim=False)
    plotMelSpec(tempo, beats, log_S, sr_data, data_name)

    return (tempo, beats, log_S, sr_data)

def plotMelSpec(tempo, beats, log_S, sr_data, data_name):
    plt.figure(1, figsize=(8,5))
    librosa.display.specshow(log_S, sr=sr_data, x_axis='time', y_axis='mel')
    plt.vlines(librosa.frames_to_time(beats),1, 0.5 * 44100, colors='w', linestyles='-', linewidth=2, alpha=0.15)
    #plt.axis('tight')
    #plt.xlim(0, 10)  
    #plt.autoscale(tight=True)
    plt.colorbar(format='%+02.0f dB')
    plt.tight_layout()
    plt.xlabel('Time (s)',fontsize='18')
    plt.ylabel('Frequency (Hz)', fontsize='18')
    #plt.title('Mel Power Spectrogram', fontsize='18')
    plt.savefig('../figures/fig_%s.png' % ('mel'))
    plt.clf()
    # print('Estimated tempo:        %.2f BPM' % tempo)
    # print('First 5 beat frames:   ', beats[:5])
    # print('First 5 beat times:    ', librosa.frames_to_time(beats[:5], sr=sr_data))

def PitchRange(data_name):
    x, sr = librosa.load(data_name) 
    acf = np.correlate(x, x, mode='full')[len(x)-1:]
    m = 1
    peaks_y=[]
    peaks_x=[]
    for K in range(len(acf)-1):
        if K > 0:
            if acf[K-1]==1:
                peaks_y.append(acf[K])
                peaks_x.append(K)
                m=m+1
            if (acf[K+1] < acf[K]) and (acf[K-1] < acf[K]):
                peaks_y.append(acf[K])
                peaks_x.append(K)
                m=m+1
            else:
                None
    print(len(acf),len(peaks_y),len(peaks_x))
    T = []
    P = []
    N=2^10
    for K in range(len(peaks_y)-1):
        T.append(abs(peaks_x[K]-peaks_x[K+1])) #Time delay
        P.append(1/T[K]) #pitch
    pitch_m=1/N*(sum(P))
    temp4=0
    for K in range(len(P)):
        temp3=(P[K]-pitch_m)**2
        temp4=temp3+temp4  
    pitch_std=((1/(N-1))*(temp4))**(1/2)
    temp2=range(len(P))
    plotPitchRange(temp2, P, data_name)
    return(P)

def plotPitchRange(temp2, P, data_name):
    plt.figure(2)
    label_A=plt.plot(temp2, np.dot(P,10**3),'.')
    plt.ylabel('Frequency (Hz)',fontsize='18')
    plt.xlabel('Number of segments',fontsize='18')
    #plt.title('Tonos calculados usando la ACF',fontsize='18')
    plt.rcParams["figure.figsize"] = (8,5)
    #plt.setp(label_A, 'label', 'Pitch range', 'color', '#1a237e')
    plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
    plt.savefig('../figures/fig_%s.png' % ('pitch'))
    plt.clf()





def MelSpectogram_db(data_name):
    sr_data = db.get_fs(data_name)
    y_data = db.get_data(data_name)
    y_harmonic, y_percussive = librosa.effects.hpss(y_data)
    S = librosa.feature.melspectrogram(y_data, sr=44100, n_mels=128)
    log_S = librosa.power_to_db(S, ref=np.max)
    tempo, beats = librosa.beat.beat_track(y=y_percussive, sr=44100, trim=False)
    plotMelSpec(tempo, beats, log_S, sr_data, data_name)

    return (tempo, beats, log_S, sr_data)


def PitchRange_db(data_name):

    sr = db.get_fs(data_name)
    x = db.get_data(data_name)

    x, sr = librosa.load(data_name) 
    acf = np.correlate(x, x, mode='full')[len(x)-1:]
    m = 1
    peaks_y=[]
    peaks_x=[]
    for K in range(len(acf)-1):
        if K > 0:
            if acf[K-1]==1:
                peaks_y.append(acf[K])
                peaks_x.append(K)
                m=m+1
            if (acf[K+1] < acf[K]) and (acf[K-1] < acf[K]):
                peaks_y.append(acf[K])
                peaks_x.append(K)
                m=m+1
            else:
                None
    print(len(acf),len(peaks_y),len(peaks_x))
    T = []
    P = []
    N=2^10
    for K in range(len(peaks_y)-1):
        T.append(abs(peaks_x[K]-peaks_x[K+1])) #Time delay
        P.append(1/T[K]) #pitch
    pitch_m=1/N*(sum(P))
    temp4=0
    for K in range(len(P)):
        temp3=(P[K]-pitch_m)**2
        temp4=temp3+temp4  
    pitch_std=((1/(N-1))*(temp4))**(1/2)
    temp2=range(len(P))
    plotPitchRange(temp2, P, data_name)
    return(P)