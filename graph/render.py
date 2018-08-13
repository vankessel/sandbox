import sys
import moviepy.editor as mpy

def create_gif(name, file_list, fps=24):
    clip = mpy.ImageSequenceClip(file_list, fps=fps)
    clip.write_gif('{}.gif'.format(name), fps=fps)

def create_webm(name, file_list, fps=24, bitrate='8192k'):
    clip = mpy.ImageSequenceClip(file_list, fps=fps)
    clip.write_videofile('{}.webm'.format(name), fps=fps, bitrate=bitrate)
