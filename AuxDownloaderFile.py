import pytube
from pytube.cli import on_progress
import pafy
from datetime import timedelta
from tqdm import tqdm
from time import sleep
import ffmpeg
import shutil
import os

#Default paths, change them if you prefer to store downloads elsewhere
music_output_path = "./Musics/"
video_output_path = "./Videos/"
temp_path = "./Temp/"

def onlyAudio(yt, titleVideo, isPlaylist, playlistTitle, channelTitle):
    if not (isPlaylist):
        audio_streams = yt.streams.get_audio_only()
        formatedChannelName = "".join( x for x in channelTitle if (x.isalnum() or x in "._- ,()"))
        audio_streams.download(filename = titleVideo + ".mp3", output_path = music_output_path + formatedChannelName)
        print("\nDownload finished!")
        return
    else:
        exit()

def highestQualityVideo(yt, titleVideo, isPlaylist, playlistTitle, channelTitle):
    #Searches for the highest resolution available stream (without audio because the highest resolution streams never have audio) 
    
    highestQualityVideo_streams = yt.streams.filter(progressive=False).order_by('resolution').desc().first() 
    print(highestQualityVideo_streams)
    highestQualityVideo_streams.download(filename = titleVideo + ".mp4", output_path = temp_path)
        
    #Searches for the highest quality audio
    highestQualityAudio_streams = yt.streams.get_audio_only()
    highestQualityAudio_streams.download(filename = titleVideo + ".mp3", output_path = temp_path)
        
    #Merges video w/ audio
    ffmpeg_video = ffmpeg.input(temp_path+titleVideo+".mp4")
    ffmpeg_audio = ffmpeg.input((temp_path+titleVideo+".mp3"))
    try:
        if isPlaylist:
           exit()
        else:
            formatedChannelName = "".join( x for x in channelTitle if (x.isalnum() or x in "._- ,()"))
            outputChannelHQPath = video_output_path +  "[HQ]" + formatedChannelName
            if not os.path.exists(outputChannelHQPath):
                os.makedirs(outputChannelHQPath)
            ffmpeg.concat(ffmpeg_video, ffmpeg_audio, v=1, a=1).output(outputChannelHQPath + "/[HQ] " + titleVideo+ ".mp4").run()
    except Exception as e:
        print(e)
        print("There was an error downloading the video, please try again")
            
        #delete temp folder
        if (os.path.exists(temp_path)):
            shutil.rmtree(temp_path)
        main()

def averageQualityVideo(yt, titleVideo, isPlaylist, playlistTitle, channelTitle):
    averageQuality_streams = yt.streams.filter(progressive=True).order_by('resolution').desc()
    print(averageQuality_streams)
    if not isPlaylist:
        formatedChannelName = "".join( x for x in channelTitle if (x.isalnum() or x in "._- ,()"))
        averageQuality_streams.first().download(filename = "[AQ] " + titleVideo + ".mp4", output_path = video_output_path  +  "[AQ] " + formatedChannelName)
    else:
        exit()

def lowestQualityVideo(yt, titleVideo, isPlaylist, playlistTitle, channelTitle):
    #Progressive contains both video and audio
    lowestQuality_stream = yt.streams.filter(progressive=True).order_by('resolution').asc().first() 
    print(lowestQuality_stream)
    if not isPlaylist:
        formatedChannelName = "".join( x for x in channelTitle if (x.isalnum() or x in "._- ,()"))
        lowestQuality_stream.download(filename = "[LQ] " + titleVideo + ".mp4", output_path = video_output_path + "[LQ] " + formatedChannelName)
    else:
        exit()


def main():

    #TODO possibilidade de procurar por nome e aparecer primeiro video?

    #ask for the link from user
    videoLink = input("What is the URL/title of the video/playlist you wish to download:  ")
    
    if((("https://y" in videoLink) or ("https://www" in videoLink)) and ("/playlist?list=" not in videoLink) and (("list" not in videoLink) or ("/watch" not in videoLink))): #If it isnt a playlist
        print("Video")
        yt = pytube.YouTube(videoLink, on_progress_callback=on_progress)
        ytPafy = pafy.new(videoLink)

        #METAINFO from the video with pytube
        print("Video Title: ",yt.title)
        print("Views: ",yt.views)
        print("Length: ",str(timedelta(seconds=yt.length)))
        print("Author: ",yt.author)
        print("Published on: " + str(yt.publish_date.strftime('%d-%m-%Y')))

        #METAINFO with pafy (some were misssing on pytube)
        print("Likes: " + str(ytPafy.likes))
        print("Dislikes: " + str(ytPafy.dislikes))
        print("====")
        print("Description: ",yt.description)
        print("====")

        #Check if you want to download Audio only or Video
        #1 = Audio only
        #2 = Video
        print("Only audio? Press 1\nHighest quality video? Press 2\nAverage quality video? Press 3\nLowest quality video? Press 4\nQuit? Press 5")
        choice = int(input())
        
        titleVideo = "".join( x for x in yt.title if (x.isalnum() or x in "._- ,()"))

        #Only audio
        if(choice == 1):
            onlyAudio(yt, titleVideo, False, None)
        
        #TODO No caso do video, falta fazer a verificacao de resolucoes mais altas, fazer merge com ffmpeg do audio e do video e apagar aux
        #TODO playlists tbm para videos

        #Highest quality video
        elif(choice == 2):  
            #Searches for the highest resolution available stream (without audio because the highest resolution streams never have audio)
            highestQualityVideo(yt, titleVideo, False, None)
        
        #Average quality video
        elif(choice == 3):
            averageQualityVideo(yt, titleVideo, False, None)

        #Lowest quality video
        elif(choice == 4):
            lowestQualityVideo(yt, titleVideo, False, None)

        #Quit
        elif (choice == 5):
            print("Bye!")
            exit()
            return
        
        else:
            print("Wrong input :(\nTry again")
            main()

            
        #delete temp folder
        if (os.path.exists(temp_path)):
            shutil.rmtree(temp_path)

        print("\nDownload finished!")
        print("Do you want to continue downloading?\nIf yes, press 1\nIf not, press 2")
        lastChoice = int(input())
        if(lastChoice == 1):
            main()
        elif(lastChoice == 2):
            print("Bye!")
            exit()
            return
        else:
            print("Wrong input :(\nTry again")
            main()
    
    elif ((("https://y" in videoLink) or ("https://www" in videoLink)) and ("/playlist?list=" in videoLink) or (("list" in videoLink) and ("/watch" in videoLink))): #If it is playlist
        ytPlaylist = pytube.Playlist(videoLink)
        print("Playlist Title: " + ytPlaylist.title)
        print("\nOnly audios? Press 1\nHigh quality videos? Press 2\nAverage quality videos? Press 3\nLowest quality videos? Press 4\nQuit? Press 5")
        playlistChoice = int(input())
        #Create folder for playlist
        for url in ytPlaylist.video_urls:
            try:
                yt = pytube.YouTube(url)
                print(yt.title)
            except VideoUnavailable:
                print('Video ' + yt.title + ' is unavailable, skipping.')
            else:
 
                #Correct format to use as file names        
                individualVideoTitle = "".join( x for x in yt.title if (x.isalnum() or x in "._- ,()"))
                
                if(playlistChoice == 1):
                    onlyAudio(yt, individualVideoTitle, True, ytPlaylist.title)
                elif(playlistChoice == 2):
                    highestQualityVideo(yt, individualVideoTitle, True, ytPlaylist.title)
                elif(playlistChoice == 3):
                    averageQualityVideo(yt, individualVideoTitle, True, ytPlaylist.title)
                elif(playlistChoice == 4):
                    lowestQualityVideo(yt, individualVideoTitle, True, ytPlaylist.title)
                elif(playlistChoice == 5):
                    print("Bye!")
                    exit()
                    return
                else:
                    print("Wrong input :(\nTry again")
                    main()
                
        if (os.path.exists(temp_path)):
            shutil.rmtree(temp_path)

        print("\nDownload finished!")
        print("Do you want to continue downloading?\nIf yes, press 1\nIf not, press 2")
        lastChoice = int(input())
        if(lastChoice == 1):
            main()
        elif(lastChoice == 2):
            print("Bye!")
            exit()
            return
        else:
            print("Wrong input :(\nTry again")
            main()

            #print('Downloading video: ' + yt.title) #tratar de download
            #yt.streams.first().download()
        

    else: #if just words
        ytSearch = pytube.Search(videoLink)
        print (ytSearch.results[0]) #most likely
        video = ytSearch.results[0]
        #METAINFO from the video with pytube
        print("Video Title: ",video.title)
        print("Views: ",video.views)
        print("Length: ",str(timedelta(seconds=video.length)))
        print("Author: ",video.author)
        print("Published on: " + str(video.publish_date.strftime('%d-%m-%Y')))
        print("====")
        print("Description: ",video.description)
        print("====")
        print("Only audio? Press 1\nHighest quality video? Press 2\nAverage quality video? Press 3\nLowest quality video? Press 4\nQuit? Press 5")
        choice = int(input())

        titleVideo = "".join( x for x in yt.title if (x.isalnum() or x in "._- ,()"))    

        #Only audio
        if(choice == 1):
            onlyAudio(video, titleVideo, False, None)
        #Highest quality video
        elif(choice == 2):  
            #Searches for the highest resolution available stream (without audio because the highest resolution streams never have audio)
            highestQualityVideo(video, titleVideo, False, None)
        #Average quality video
        elif(choice == 3):
            averageQualityVideo(video, titleVideo, False, None)
        #Lowest quality video
        elif(choice == 4):
            lowestQualityVideo(video, titleVideo, False, None)
        #Quit
        elif (choice == 5):
            print("Bye!")
            exit()
            return
        else:
            print("Wrong input :(\nTry again")
            main() 
        #delete temp folder
        if (os.path.exists(temp_path)):
            shutil.rmtree(temp_path)

        print("\nDownload finished!")
        print("Do you want to continue downloading?\nIf yes, press 1\nIf not, press 2")
        lastChoice = int(input())
        if(lastChoice == 1):
            main()
        elif(lastChoice == 2):
            print("Bye!")
            exit()
            return
        else:
            print("Wrong input :(\nTry again")
            main()
        pass

if __name__ == "__main__":
    try:
        main()
    except IndexError:
        print("\tError executing the script")
