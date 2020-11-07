import os, sys, pathlib, vlc, platform
import tkinter as tk
from tkinter import filedialog

class BaseTkContainer:
    def __init__(self):
        self.tk_instance = tk.Tk()
        self.tk_instance.title("Media Player")
        self.tk_instance.geometry("640x510")
        self.tk_instance.protocol("WM_DELETE_WINDOW", self.onCloseWindow)
        #self.tk_instance.configure(background='black')
        # Create Video panel
        self.videoFrame = tk.LabelFrame(self.tk_instance, relief=tk.GROOVE, bg="blue")
        self.videoFrame.pack(fill=tk.BOTH, expand=True)
        # Create Control and Display panel
        controlFrame = tk.LabelFrame(self.tk_instance, relief=tk.GROOVE, bg='#383859')
        #controlFrame.place(x=0, y=480, width=640, height=30)
        controlFrame.pack(fill=tk.X, padx=5, pady=5)
        openBtn = tk.Button(controlFrame, text="Open", command=self.OpenFile, bd=0).grid(row=0, column=0, sticky=tk.W)
        playBtn = tk.Button(controlFrame, text="Play", command=self.PlayMovie, bd=0).grid(row=0, column=1, sticky=tk.W)
        pauseBtn = tk.Button(controlFrame, text="Pause", command=self.PauseMovie, bd=0).grid(row=0, column=2, sticky=tk.W)
        stopBtn = tk.Button(controlFrame, text="Stop", command=self.StopMovie, bd=0).grid(row=0, column=3, sticky=tk.W)
        testBtn = tk.Button(controlFrame, text="Time", command=self.InfoDisplay, bd=0).grid(row=0, column=5, sticky=tk.W)
        self.timeLabel = tk.Label(controlFrame, font=("calibri",11,"bold"))
        self.nameLabel = tk.Label(controlFrame, font=("calibri",11,"bold"))
        self.volumeScale = tk.Scale(controlFrame, from_=0, to=100, orient=tk.HORIZONTAL, 
                                    command=self.MovieVolume, sliderlength=15, bd=0, showvalue=0, length=200)
        self.volumeScale.grid(row=0, column=4, sticky=tk.W)
        self.volumeScale.set(50)

    def onCloseWindow(self):
        try:
            self.mediaPlayer.stop()
        except:
            pass
        self.tk_instance.destroy()
    
    def MovieVolume(self, setValue):
        """Volume settings"""
        volume = self.volumeScale.get()
        try:
            self.mediaPlayer.audio_set_volume(volume)
        except AttributeError:
            pass

    def PlayMovie(self):
        """Play a file"""
        self.mediaPlayer.play()
        self.mediaPlayerState = "State.Playing"
        self.InfoDisplay()

    def StopMovie(self):
        """Stop the player"""
        self.mediaPlayer.stop()

    def PauseMovie(self):
        """Pause the player"""
        self.mediaPlayer.pause()

    def OpenFile(self):
        """Open window explorer to select a movie to play"""
        file = filedialog.askopenfilename()
        directoryName = os.path.dirname(file)
        self.fileName = os.path.basename(file)
        media = str(os.path.join(directoryName, self.fileName))
        self.mediaPlayer = vlc.MediaPlayer(media)
        # set the window id where to render VLC's video output
        if platform.system() == 'Windows':
            self.mediaPlayer.set_hwnd(self.GetHandle())
        else:
            self.mediaPlayer.set_xwindow(self.GetHandle())

    def InfoDisplay(self):
        """Display basic info about a movie"""
        pass

    def GetHandle(self):
        return self.videoFrame.winfo_id()

if __name__ == "__main__":
    root = BaseTkContainer()
    root.tk_instance.mainloop()
