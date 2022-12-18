from kivy.app import App
from kivy.uix.screenmanager import ScreenManager ,Screen
from kivy.core.image import Image as CoreImage
from kivy.uix.boxlayout import BoxLayout 
from kivy.uix.button import ButtonBehavior ,Button
from kivy.core.audio import SoundLoader
from kivy.core.window import Window
from kivy.graphics import *
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.uix.widget import Widget

from player import SoundAndroidPlayer
import audio_metadata 


from os import walk
import threading
import io

player = SoundAndroidPlayer()

def get_kivy_image_from_bytes(image_bytes, file_extension):
	buffer = io.BytesIO(image_bytes)
	base = CoreImage(buffer ,ext=file_extension)
		
	return base
	       								

class Manager(ScreenManager):
	
	...
	
class ScreenSelectSongs(Screen):
	path = walk("/storage/emulated/0/")
	files = []
	pictureCurrent = Image()
	songCurrent = None
	artistCurrent = None
	def __init__(self ,**kwargs):
		super(ScreenSelectSongs ,self).__init__(**kwargs)
		
		Clock.schedule_once(self.updateList)
		
	def updateList(self ,*args):
	   th = threading.Thread(target=self.addh ,args=[])
	   th.start()
	   
	def addh(self):
	   index = 0
	   bar_options = PlayerOptionsBar()
	   self.add_widget(bar_options)
	   print(bar_options)
	   for subdir ,_ ,files in self.path:
	       for file in files:
	       	if file.endswith(".mp3"):
	       		path = str(subdir + "/" + file)
	       		btn = StyleSelectButton(path ,bar_options ,index ,self)
	       		self.ids.select_box.add_widget(btn)
	       		self.files.append(file)
	       		index += 1
	   
	   self.ids.select_box.add_widget(Widget(size_hint_y = None ,height = "70dp"))
	  				       																	
class StyleSelectButton(ButtonBehavior ,BoxLayout):
	picture_pattern = None
	path = None
	bar = None
	title = None
	artist = None
	index = 0
	def __init__(self ,path ,bar ,index ,root,**kwargs):
		super(StyleSelectButton ,self).__init__(**kwargs)
		self.path = path
		self.index = index
		self.bar = bar
		self.root = root
		Clock.schedule_once(self.update)
		
	def update(self ,*args):
		
		try:
		    meta = audio_metadata.load(self.path)
		    self.artist = meta["tags"]["artist"]
		    self.title = meta["tags"]["title"]
		    bytes_picture = meta["pictures"][0]["data"]
		    self.picture_pattern =  get_kivy_image_from_bytes(bytes_picture,"jpg")
		   
		except:
			file = self.root.files#[self.index]
		
			self.title = file[0:len(file[self.index])-3]
			print(self.title)
			self.artist = "<Unknown>".split()
			self.picture_pattern = Image(source="b.png")
		
		self.ids.artist.text = self.artist[0]
		self.ids.title.text =  self.title[0][0:37] + "..." if len(self.title[0]) >= 37 else self.title[0]
		self.ids.pic.texture = self.picture_pattern.texture
		
	def on_press(self):
		self.root.songCurrent = self.title[0][0:37] + "..." if len(self.title[0]) > 37 else self.title[0]
		self.root.artistCurrent = self.artist[0]
		self.root.pictureCurrent = self.picture_pattern
		self.bar.start(pic = self.picture_pattern ,title = self.title ,artist= self.artist)
		player.load(self.path)
		self.root.parent.current = "playing"
	def on_release(self):
		self.bar.y = 0
		player.play()

class ScreenPlaySongs(Screen):
	
	def __init__(self ,**kwargs):
		super(ScreenPlaySongs ,self).__init__(**kwargs)
		
		Window.bind(on_keyboard=self.android_back_click)
		
	def android_back_click(self,window,key,*args):
        
         if  key == 27:
             try:
                 self.parent.current = "select"
             except AttributeError:
                 pass
             return True
	
	def on_pre_enter(self):
		self.root = self.parent.get_screen("select")
		self.ids.play_pic.texture = self.root.pictureCurrent.texture
		self.ids.title.text = self.root.songCurrent
		self.ids.artist.text = self.root.artistCurrent

class PlayerOptionsBar(BoxLayout,Button):
	def on_press(self):
		self.parent.parent.current = "playing"
	def start(self ,pic ,title ,artist):
		self.ids.pic_bar.texture = pic.texture
		self.ids.title_bar.text = title[0][0:37] + "..." if len(title[0]) > 37 else title[0]
		self.ids.artist_bar.text = artist[0]
class TheWinePlayer(App):

	def build(self):
		
		return Manager()
		
if __name__ == "__main__":
		SoundLoader.register(SoundAndroidPlayer) 
		TheWinePlayer().run()
			