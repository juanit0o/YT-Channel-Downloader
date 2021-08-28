import pytube
from pytube.cli import on_progress
import pafy
from datetime import timedelta
from tqdm import tqdm
from time import sleep
import ffmpeg
import shutil
import os
import AuxDownloaderFile as YT_Downloader


#Default paths, change them if you prefer to store downloads elsewhere
music_output_path = "./Musics/"
video_output_path = "./Videos/"
temp_path = "./Temp/"

def auxMet():
    print("Which channel do you want to download videos from?")
    channelInput = input()
    try:
        channel = pytube.Channel(channelInput)
    except:
        print("Wrong format, enter the channel link!")
        auxMet()

    print("Channel name: " + channel.channel_name)
    print("Number of videos " + str(len(channel.video_urls)))
    print("Do you want to download all of the channel videos? Press 1\nDo you want to download only X latest videos? Press 2")
    choiceAll = int(input())
    if(choiceAll == 1):
        print("Do you really wish to download all the videos in the channel?\nPress 1, if yes\nPress 2, if not")
        choiceDownload = int(input())
        if(choiceDownload == 1):
            print("Only audio? Press 1\nHighest quality video? Press 2\nAverage quality video? Press 3\nLowest quality video? Press 4\nQuit? Press 5")
            choice = int(input())
            for video in channel.video_urls:
                downloads(video, choice, channel.channel_name)
            print("Do you want to continue downloading?\nIf yes, press 1\nIf not, press 2")
            lastChoice = int(input())
            if(lastChoice == 1):
                auxMet()
            elif(lastChoice == 2):
                print("Bye!")
                exit()
                return
            else:
                print("Wrong input :(\nTry again")
                auxMet()
        elif(choiceDownload == 2):
                print("Bye!")
                exit()
                return
        else:
            print("Wrong input :(\nTry again")
            auxMet()

    elif (choiceAll == 2):
        print("How many latest videos do you want to download?")
        nrVideos = int(input())
        print("Only audio? Press 1\nHighest quality video? Press 2\nAverage quality video? Press 3\nLowest quality video? Press 4\nQuit? Press 5")
        choice = int(input())
        
        if (choice == 5):
            print("Bye!")
            exit()
        else:
            nrDownloaded = 0
            for i in range(nrVideos):
                if(nrDownloaded >= len(channel.video_urls)):
                    print("You selected more videos than what the channel had posted but I downloaded all of them!\n")
                    break  
                downloads(channel.video_urls[i], choice, channel.channel_name)
                nrDownloaded+=1

            print("Do you want to continue downloading?\nIf yes, press 1\nIf not, press 2")
            lastChoice = int(input())
            if(lastChoice == 1):
                auxMet()
            elif(lastChoice == 2):
                print("Bye!")
                exit()
            else:
                print("Wrong input :(\nTry again")
                auxMet()
    
    elif(choiceAll == 3):
        print("Bye!")
        exit()
    else:
        print("Wrong input :(\nTry again")
        auxMet()

def downloads(url, choice, channelTitle):  
    if((("https://y" in url) or ("https://www" in url)) and ("/playlist?list=" not in url) and (("list" not in url) or ("/watch" not in url))): #If it isnt a playlist
        print("Video")

        yt = pytube.YouTube(url)

        #METAINFO from the video with pytube
        print("Video Title: ",yt.title)
        print("Views: ",yt.views)
        print("Length: ",str(timedelta(seconds=yt.length)))
        print("Author: ",yt.author)
        print("Published on: " + str(yt.publish_date.strftime('%d-%m-%Y')))

        print("====")
        print("Description: ",yt.description)
        print("====")

        #Correct format to use as file names        
        titleVideo = "".join( x for x in yt.title if (x.isalnum() or x in "._- ,()"))

        #Only audio
        if(choice == 1):
            YT_Downloader.onlyAudio(yt, titleVideo, False, None, channelTitle)
        
        #Highest quality video
        elif(choice == 2):  
            #Searches for the highest resolution available stream (without audio because the highest resolution streams never have audio)
            YT_Downloader.highestQualityVideo(yt, titleVideo, False, None, channelTitle)
        
        #Average quality video
        elif(choice == 3):
            YT_Downloader.averageQualityVideo(yt, titleVideo, False, None, channelTitle)

        #Lowest quality video
        elif(choice == 4):
            YT_Downloader.lowestQualityVideo(yt, titleVideo, False, None, channelTitle)

        #Quit
        elif (choice == 5):
            print("Bye!")
            exit()
            return
        
        else:
            print("Wrong input :(\nTry again")
            auxMet()

            
        #delete temp folder
        if (os.path.exists(temp_path)):
            shutil.rmtree(temp_path)


auxMet()