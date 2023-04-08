from youtube_transcript_api import YouTubeTranscriptApi
import translators.server as tss
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.clock import Clock

from_language, to_language = 'en', 'ro'


class Traducator(App):
    def build(self):
        self.window = GridLayout()
        self.window.cols = 1

        self.youtubelink = Label(text="Input youtube link:")
        self.userinput = TextInput(multiline=False)
        self.startbutton = Button(text="Start!", size_hint=(1, 0.5))
        self.transcribebutton = Button(text="Wait...")
        self.script = Label(text="", valign="top")
        self.pausebutton = Button(text="Pause", size_hint=(0.3,0.2))
        self.j = []

        self.startbutton.bind(on_press=self.callback)
        self.pausebutton.bind(on_press=self.pause)

        self.window.add_widget(self.youtubelink)
        self.window.add_widget(self.userinput)
        self.window.add_widget(self.startbutton)

        return self.window

    def callback(self, instance):
        self.userinput.text = self.userinput.text.split("e/")[1]
        Clock.schedule_once(self.clear, 0)
        Clock.schedule_once(self.add1, 0)
        Clock.schedule_once(self.do_transcription, 1)

    def do_transcription(self, instance):
        self.full = YouTubeTranscriptApi.get_transcript(self.userinput.text)
        for i in self.full:
            self.j.append({"text": tss.google(i['text'], from_language, to_language), "start": i['start']})
        Clock.schedule_once(self.add3, 0)

    def add1(self, instance):
        self.window.add_widget(self.transcribebutton)

    def add3(self, instance):
        self.transcribebutton.text = "Press to start transcription!"
        self.transcribebutton.bind(on_press=self.afisare)

    def afisare(self, instance):
        Clock.schedule_once(self.clear, 0)
        Clock.schedule_once(self.add2, 0)
        self.script.valign = "top"
        self.i = 0
        Clock.schedule_once(self.afisare1, 0)

    def afisare1(self, instance):
        if self.i>=len(self.j):
            return False
        t1 = self.j[self.i]['start']
        self.script.text += self.j[self.i]['text'] + '\n'
        self.script.halign = "left"
        self.i += 1
        if self.i < len(self.j):
            t2 = self.j[self.i]['start']
        else:
            t2 = 0
        Clock.schedule_once(self.afisare1, t2 - t1)

    def clear(self, instance):
        self.window.clear_widgets()

    def add2(self, instance):
        self.window.add_widget(self.script)
        self.window.add_widget(self.pausebutton)

    def pause(self, instance):
        if self.pausebutton.text == "Pause":
            self.pausebutton.text="Unpause"
            Clock.schedule_once(self.unpause, 0)
        else:
            self.pausebutton.text="Pause"

    def unpause(self, instance):
        Clock.schedule_once(self.unpause, 0)


if __name__ == "__main__":
    Traducator().run()
