!pip install moviepy
!pip install pytube

import moviepy
import argparse
from pytube import YouTube
from moviepy.editor import *
import lxml
from lxml import etree
import os

VIDEO_SAVE_DIRECTORY = "Your_Video_Directory_Here"

def download(video_url):
    video = YouTube(video_url)
    video = video.streams.get_highest_resolution()

    try:
        video.download(VIDEO_SAVE_DIRECTORY)
    except:
        print("Failed to download video")

    print("video was downloaded successfully")

    youtube = etree.HTML(urllib.urlopen(video_url).read()) //enter your youtube url here
    video_title = youtube.xpath("//span[@id='eow-title']/@title") 
    return ''.join(video_title)
  
link = "YouTube Link Here"

video_storage_location = os.path.join(VIDEO_SAVE_DIRECTORY, download(link), '.mp4')



from moviepy.editor import *

def mash(source_video_adress, req_vid_dur = 300, clip_max_dur=5):
  
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

    if random.choices([0,1], weights = [1,2], k = 1)[0] == 0:
      pass
      clip = clip.rotate(180)

    clip_list.append(clip)

    out_vid_dur = out_vid_dur + clip_duration
    print("Start = {}, Duration = {}, Total = {}".format(clip_start_timestamp, clip_duration, out_vid_dur))

  merged_video=moviepy.editor.concatenate_videoclips(clip_list)
  print(merged_video.duration)

  merged_video.write_videofile(
                              "output_video.mp4",
                               codec='libx264'
                               )
  return duration

mash(video_adress, req_vid_dur = 180, clip_max_dur = 5 )

