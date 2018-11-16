from scipy import signal
import matplotlib.pyplot as plt
from scipy.io import wavfile


def spectrogram_gen (audio_file, fig_id):
    
    #Reading song
    fs, data = wavfile.read(audio_file)
    
    #Hanning window, 8192 points and 0.75 overlap as in [22]
    f, t, Sxx = signal.spectrogram(data, fs, window=('hann'),nperseg=8192 ,noverlap=0.75) 
    plt.pcolormesh(t, f, Sxx)
    plt.ylim(top=650)  # adjust the top leaving bottom unchanged
    plt.ylim(bottom=20)
    plt.ylabel('Frequency [Hz]', fontsize = 18)
    plt.xlabel('Time [sec]',fontsize = 18)
    #plt.axis('off')
    plt.savefig('../figures/fig_%s.png' % (fig_id), bbox_inches= 'tight')





