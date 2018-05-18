from __future__ import unicode_literals

import os
import sys
import youtube_dl
import time
import keyboard

from threading import Thread
from WSP import WinSoundPlayer


class yt_player(object):

    def __init__(self, url, opts=None, dir=None, auto_del=True):
        self.current_sound = None
        self.auto_del = auto_del
        self.lector = None
        self.dir = dir
        self.url = url
        self.opts = opts
        if dir:
            self.opts['outtmpl'] = dir + '%(title)s.%(ext)s'
        else:
            dir = ""
        self.available_music = []
        keyboard.add_hotkey('ctrl+n', self._change)

    def download(self):
        with youtube_dl.YoutubeDL(self.opts) as ydl:
            ydl.download([self.url])

    def check_webm(self):
        d = os.listdir(self.dir)
        for f in d:
            if ".webm" in f:
                return f.replace(".webm", "")

    def check_mp3(self):
        d = os.listdir(self.dir)
        for f in d:
            if ".mp3" in f:
                if self.dir+f not in self.available_music:
                    dlf = self.check_webm()
                    if not dlf:
                        self.available_music.append(self.dir+f)
                    elif f.replace(".mp3", "") not in dlf:
                        self.available_music.append(self.dir+f)

    def _change(self):
        self.change = True

    def play(self):
        self.is_reading = True
        self.change = False
        self.is_playing = False
        while self.is_reading:
            self.check_mp3()
            if not self.is_playing and len(self.available_music) > 0:
                self.current_music = self.available_music[0]
                self.lector = playsound(self.current_music, block=False)
                self.lector.play_sound()
                self.is_playing = True
            if self.change and self.lector:
                self.lector.stop_sound()
                self.change = False
                self.is_playing = False
                if self.auto_del:
                    os.remove(self.available_music[0])
                self.available_music.pop(0)

    def start(self):
        Thread(target=self.play).start()



if  __name__ == '__main__':

    url = "https://www.youtube.com/watch?v=FHccClTAdzc&index=0&list=RDS76rZVz0Wf8"

    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
        }],
    }
    # Absolute path
    dir = "C:/Users/music/"
    if not os.path.exists(dir):
        os.mkdir(dir)

    try:
        p = yt_player(url, opts=ydl_opts, dir=dir)
        p.start()
        p.download()
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        p.is_reading = False
        d = os.listdir(dir)
        for f in d:
            if ".mp3" in f or ".webm" in f:
                os.remove(dir+f)
        sys.exit(0)
