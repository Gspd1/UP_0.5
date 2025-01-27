import vlc

import tkinter as tk

from tkinter import filedialog

class VideoPlayer:

    def __init__(self, root):

        self.root = root

        self.root.title("Video Player")

        # Создаем кнопки

        self.play_button = tk.Button(root, text="Play", command=self.play_video)

        self.play_button.pack()

        self.stop_button = tk.Button(root, text="Stop", command=self.stop_video)

        self.stop_button.pack()

        self.load_button = tk.Button(root, text="Load Video", command=self.load_video)

        self.load_button.pack()

        # Инициализация VLC

        self.vlc_instance = vlc.Instance()

        self.player = self.vlc_instance.media_player_new()

    def load_video(self):

        # Открытие диалогового окна для выбора файла

        file_path = filedialog.askopenfilename(filetypes=[("Video Files", "*.mp4;*.mkv;*.avi")])

        if file_path:

            media = self.vlc_instance.media_new(file_path)

            self.player.set_media(media)

    def play_video(self):

        if self.player.get_media() is not None:

            self.player.play()

    def stop_video(self):

        self.player.stop()

if __name__ == "__main__":

    root = tk.Tk()

    video_player = VideoPlayer(root)

    root.mainloop()
