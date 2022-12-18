from jnius import autoclass
from kivy.core.audio import Sound

MediaPlayer = autoclass("android.media.MediaPlayer")
FileInputStream = autoclass("java.io.FileInputStream")
AudioManager = autoclass("android.media.AudioManager")

class SoundAndroidPlayer(Sound):
    @staticmethod
    def extensions():
        return ("mp3", "mp4", "aac", "3gp", "flac", "mkv", "wav", "ogg")

    def __init__(self, **kwargs):
        self._mediaplayer = None
        super(SoundAndroidPlayer, self).__init__(**kwargs)
        pass

    def load(self,filename=""):
        self.unload()
        self._mediaplayer = MediaPlayer()
        self._mediaplayer.setAudioStreamType(AudioManager.STREAM_MUSIC)
        self._mediaplayer.setDataSource(filename)
      
        self._mediaplayer.prepare()

    def unload(self):
        self.stop()
        self._mediaplayer = None

    def play(self):
        if not self._mediaplayer:
            return
        self._mediaplayer.start()
        super(SoundAndroidPlayer, self).play()

    def stop(self):
        if not self._mediaplayer:
            return
        self._mediaplayer.reset()
        
    def pause(self):
        if not self._mediaplayer:
            return
        self._mediaplayer.pause()
    def repeat(self,state):
         if not self._mediaplayer:
            return
         self._mediaplayer.setLooping(state)
    def seek(self, position):
        if not self._mediaplayer:
            return
        self._mediaplayer.seekTo(float(position))

    def get_pos(self):
        if self._mediaplayer:
            return self._mediaplayer.getCurrentPosition()/1000
        return super(SoundAndroidPlayer, self).get_pos()

    def on_volume(self, instance, volume):
        if self._mediaplayer:
            volume = float(volume)
            self._mediaplayer.setVolume(volume, volume)

    def _get_length(self):
        if self._mediaplayer:
            return self._mediaplayer.getDuration()/1000
        return super(SoundAndroidPlayer, self)._get_length()