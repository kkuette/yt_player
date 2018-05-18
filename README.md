# yt_player
Minimal youtube player/downloader in python

It work with [WinSoundPlayer](https://github.com/kkuette/WinSoundPlayer) and [youtube_dl](https://github.com/rg3/youtube-dl)

## How to use
```
p = yt_player(url, opts=ydl_opts, dir=dir) # Init player opts : youtube_dl options, dir : absolute path, auto_del : del sounds after playing
p.start()                                  # Start player thread
p.download                                 # Start downloading
p.is_reading = False                       # Stop player Thread
```
