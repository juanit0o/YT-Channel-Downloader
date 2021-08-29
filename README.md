# YT-Channel-Downloader
A python application to download all of the videos posted by a Youtube channel.

It follows a similar approach to my previous Youtube Downloader where you can choose to download
* Only Audio
* Highest Quality Available video
* Average Quality Available video
* Lowest Quality Available video

It is an easy way to download all of the videos in a channel that aren't in any playlist and save them at your own liking in your computer.
You also have the option to 
* Download all of the videos
<p align="center">
       <img src="https://i.imgur.com/8rPhvgg.gif" width="450" height="250" alt="Layout of the website">
</p> 

* Download the latest X videos
<p align="center">
       <img src="https://i.imgur.com/6q7BiWA.gif" width="450" height="250" alt="Layout of the website">
</p> 

As of now, pytube has some problems in its regex searches and ability to search only by a keyword but it is being solved on their side and expected to be solved in the next version (11.0.1).

Hope you enjoy it and find it useful!

###### This was made using the pytube library and you have to have <a href=https://www.ffmpeg.org/>ffmpeg</a> installed and set in your ambient variables to download the videos in their highest resolution available.


The ffmpeg dependency is due to the fact that all of the progressive streams are limited to 720p and by downloading both video and audio separated and merging them afterwards using this library guarantees that you can download videos up to 2k and with high bitrate audio.

The downloads are saved in 2 folders which are created in the same directory that the script is run in (./Videos and ./Musics). 

If you want to change the path you can do so on the global variables on the top of the script as shown bellow.

<p align="center">
       <img src="https://i.imgur.com/rP3uzLh.png" width="500" height="100" alt="Layout of the website">
</p>

## Instructions
* Install the executable file in your computer (under the releases tab)
* Download the videos from your favourite channels!
No need to have python installed in your computer anymore, everything is packed in an executable file that can be run in any computer running Windows!

Hope you enjoy it and find it useful!


