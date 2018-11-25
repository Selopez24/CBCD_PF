from scipy import signal
import matplotlib.pyplot as plt
from scipy.io import wavfile
import librosa
from scipy.io import wavfile as wav
import features
import score
import descdb as db

def spectrogram_gen (audio_file, fig_id):
    
    #Reading song
    data, fs = librosa.load(audio_file)
    
    #Hanning window, 8192 points and 0.75 overlap as in [22]
    f, t, Sxx = signal.spectrogram(data, fs, window=('hann'),nperseg=8192 ,noverlap=0.75) 
    plt.pcolormesh(t, f, Sxx)
    plt.ylim(top=650)  # adjust the top leaving bottom unchanged
    plt.ylim(bottom=20)
    plt.ylabel('Frequency [Hz]', fontsize = 18)
    plt.xlabel('Time [sec]',fontsize = 18)
    plt.title('Spectrogram %s' % (audio_file))
    #plt.title(audio_file, fontsize = 18)
    #plt.axis('off')
    plt.savefig('../figures/fig_%s.png' % (fig_id), bbox_inches= 'tight')
    
    return data, fs




data_test , fs = spectrogram_gen('metal0.wav', 1)

data_test2 , fs = spectrogram_gen('../dataset.wav/metal.wav/metal0.wav', 4)


#rate, data = wav.read('metal0.wav')
#plt.rcParams['agg.path.chunksize'] = 10000
#plt.plot(y2)
plt.show()
#../dataset.wav/metal.wav/metal0.wav

#features.MelSpectogram('metal0.wav')
#features.PitchRange('../dataset.wav/metal.wav/metal0.wav')

a , f = score.CorrelationChroma3('../dataset.wav/metal.wav/metal0.wav', '../dataset.wav/metal.wav/metal0.wav')