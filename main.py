import os

from pydub import AudioSegment
from pytube import YouTube
from pytube.cli import on_progress
import shutil


def replaceCharacters(str):
    '''
    Drops reserved characters from string.
    Source: https://docs.microsoft.com/en-us/windows/win32/fileio/naming-a-file?redirectedfrom=MSDN
    '''
    skipChars = "`~!@#$%^&*()_+=-|}{[]\;':?></.,"
    for i in skipChars:
        if i in str:
            str = str.replace(i, '')
    return str


def download(link, downloadPath):
    '''
    Downloads YouTube video from the provided link.
    Saves to a folder named as the video title.
        Parameters:
                link (str): YouTube video link
        Returns:
                trackTitle (str): Title of the YouTube video
    '''
    def changeCompleteStatus(status):
        status = not status

    downloadStatus = False
    try:
        yt = YouTube(link, on_progress_callback=on_progress)
    except:
        print("EXCEPTION OCCURED")
    trackTitle = replaceCharacters(yt.title)
    print(f"\n---Downloading: {trackTitle}---")

    yt.register_on_complete_callback(changeCompleteStatus(downloadStatus))
    yt.streams.filter(only_audio=True)[0].download(
        f"{downloadPath}\\{trackTitle}", filename=trackTitle)
    print("\n---Download Complete!---")
    return trackTitle


def clipAudio(audioFile, timeStamp, trackTitle, downloadPath):
    '''
    Cuts an audio clip as per the time stamps provided.

    Parameters:
        audioFile (pydub.AudioSegment): Audio clip of the downloaded file
        timeStamp (str list): String list of start and end times formatted as
                                                ->mm:ss, mm:ss
        trackTitle (str): 	Title of the YouTube video				
    '''
    if not os.path.exists('./trackfiles/'+trackTitle):
        os.makedirs('./trackfiles/'+trackTitle)
    count = 0
    print("\n---Clipping Audio to Time Stamps!---")
    for line in timeStamp[1:]:
        times = line.split(',')
        start, finish = times[0], times[1]

        startMin, startSec = (start.split(':'))
        finishMin, finishSec = (finish.split(':'))

        startTime = (int(startMin) * 60 + int(startSec)) * 1000
        finishTime = (int(finishMin) * 60 + int(finishSec)) * 1000
        # try:
        cutAudio = audioFile[startTime:finishTime]
        cutAudio.export(
            f"{downloadPath}/{trackTitle}/{exportName}{count}.mp3", format="mp3")
        # except:
        #     print("Couldn't export clip of time stamp: {start}-{finish}")

        count = count + 1
    print("\n---Clipping Complete---")


if __name__ == "__main__":
    file = open('Link.txt', 'r')
    lines = file.readlines()
    link = lines[0]

    print("YouTube link received: " + link, end='')
    downloadPath = os.path.join(os.getcwd(), "downloads")

    trackTitle = download(link, downloadPath)

    reqPath = os.path.join(
        os.getcwd(), "downloads", trackTitle, trackTitle.replace(',', '') + ".mp4")
    audioFile = AudioSegment.from_file(reqPath, "mp4")

    exportName = trackTitle.split(' ')[0]
    clipAudio(audioFile, lines, trackTitle, downloadPath)
    shutil.copy2('Link.txt', os.path.join(downloadPath, trackTitle))
