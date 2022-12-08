import os
import librosa, librosa.display
import matplotlib.pyplot as plt
import sys
import pathlib
import numpy as np

def generate_mel_spectrogram(folder_path,track_name):
    if track_name.endswith('.mp3'):
        x, sr = librosa.load((folder_path/track_name).as_posix()) # librosa likes unix path system
        hop_length = 256
        S = librosa.feature.melspectrogram(x,sr=sr,n_fft=4096,hop_length=hop_length)
        logS = librosa.power_to_db(S,ref= np.max)
        fig, ax = plt.subplots()
        img = librosa.display.specshow(logS,hop_length=hop_length,x_axis='time',y_axis='mel',ax=ax)
        fig.colorbar(img,ax=ax,format='%+2.0f dB')
        fig.savefig(folder_path/'Spectrogram'/os.path.splitext(track_name)[0])

def get_tracks_spectrogram(folder_path):
    if not os.path.exists(folder_path/'Spectrogram'):
        os.makedirs(folder_path/'Spectrogram')
    for track_name in os.listdir(str(folder_path)):
        generate_mel_spectrogram(folder_path,track_name)

if __name__ == "__main__":
    root_path = pathlib.Path().absolute() / sys.argv[1] # directory path which contains folders of tracks
    for folders in os.listdir(str(root_path)):
        get_tracks_spectrogram(root_path / folders)