!wget https://repo.anaconda.com/miniconda/Miniconda3-py37_4.8.2-Linux-x86_64.sh
!chmod +x Miniconda3-py37_4.8.2-Linux-x86_64.sh
!bash ./Miniconda3-py37_4.8.2-Linux-x86_64.sh -b -f -p /usr/local
import sys
sys.path.append('/usr/local/lib/python3.7/site-packages/')
!conda install -c conda-forge ffmpeg -y
!conda remove ffmpeg -y
!sudo apt-get install ffmpeg -y
!pip install moviepy
!pip install pytube

from moviepy.editor import *
import os
import random

VIDEO_SAVE_DIRECTORY = "Your_Storage_Directory" #The downloaded video from YouTube will be stored here.

def download(video_url):
    video = YouTube(video_url)
    video = video.streams.get_highest_resolution()

    try:
        video.download(VIDEO_SAVE_DIRECTORY)
    except:
        print("Failed to download video")

    print("video was downloaded successfully")

def video_title(url):
  import requests
  from bs4 import BeautifulSoup
  r = requests.get(url)
  soup = BeautifulSoup(r.text)

  res = soup.find_all(name="title")[0]
  title = str(res)
  title = title.replace("<title>","")
  title = title.replace("</title>","")
  title = title.replace(" - YouTube", "")

  return title


def mash(youtube_link, req_vid_dur = 50, clip_max_dur=5):
  
  download(youtube_link)
  print("Video downloaded")

  title = video_title(youtube_link)
  print(f"Title extracted, title = {title}")

  source_video_adress = os.path.join(VIDEO_SAVE_DIRECTORY,title+'.mp4')
  print(source_video_adress)
  assert os.path.exists(source_video_adress)
  print("Video adress valid")

  try:
    vid_ori = VideoFileClip(source_video_adress)
  except:
    pass

  out_vid_dur = 0
  clip_list = []

  while out_vid_dur < req_vid_dur:

    clip_start_timestamp = round(random.uniform(0,vid_ori.duration-clip_max_dur),2)
    clip_duration = round(random.triangular(low = 0, high = clip_max_dur, mode = clip_max_dur/2),2)
    clip = vid_ori.subclip(clip_start_timestamp, clip_start_timestamp+clip_duration)

    if random.choices([0,1], weights = [1,2], k = 1)[0] == 0: #Remove this, this is not necessary. This will rotate a clip upside down.
      clip = clip.rotate(180)

    clip_list.append(clip)

    out_vid_dur = out_vid_dur + clip_duration
    print("Start = {}, Duration = {}, Total = {}".format(clip_start_timestamp, clip_duration, out_vid_dur))

  merged_video=moviepy.editor.concatenate_videoclips(clip_list)
  print(merged_video.duration)

  merged_video.write_videofile(
                              "output.mp4", #Output file name
                               codec='libx264'
                               )

if __name__ == '__main__':
    mash(youtube_link = "URL_of_a_YouTube_Video",
         req_vid_dur = 50, #How long should the output video be
         clip_max_dur = 5 #What should be the maximum duration of a clip during the mashup
        )
