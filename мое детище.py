import datetime
import random
import tkinter as tk
from tkinter import filedialog
from tkinter.messagebox import showinfo
from tkVideoPlayer import TkinterVideo

playlist = []
current_video_index = 0
playlist_active = False
shuffle_mode = False
repeat_one_mode = False

def update_duration(event):
    """ updates the duration after finding the duration """
    duration = vid_player.video_info()["duration"]
    end_time["text"] = str(datetime.timedelta(seconds=duration))
    progress_slider["to"] = duration


def update_scale(event):
    """ updates the scale value """
    progress_value.set(vid_player.current_duration())


def load_video():
    """ loads the video """
    file_path = filedialog.askopenfilename(filetypes=[("Video Files", "*.mp4 *.avi *.mkv")])

    if file_path:
        vid_player.load(file_path)

        progress_slider.config(to=0, from_=0)
        play_pause_btn["text"] = "Play"
        progress_value.set(0)


def my_seek(value):
    """ used to seek a specific timeframe """
    vid_player.seek(int(value))
    # file_path = filedialog.askopenfilename(filetypes=[("Video Files", "*.mp4 *.avi *.mkv")])
    # if not file_path:
    #     print('Сначала загрузите видео')


def skip(value: int):
    """ skip seconds """
    vid_player.seek(int(progress_slider.get())+value)
    progress_value.set(progress_slider.get() + value)


def play_pause():
    """ pauses and plays """
    if vid_player.is_paused():
        vid_player.play()
        play_pause_btn["text"] = "Pause"

    else:
        vid_player.pause()
        play_pause_btn["text"] = "Play"


def video_ended(event):
    """ handle video ended """
    progress_slider.set(progress_slider["to"])
    play_pause_btn["text"] = "Play"
    progress_slider.set(0)

def show_help():
    showinfo(title ="Справка", message="Инструкция пользования плеером")


root = tk.Tk()
root.title("Видеоплеер")
root.iconbitmap(default="illustration2.ico")
root.geometry("1000x600-150-90")
root.minsize(700, 400)

# Меню "Медиа"
menubar = tk.Menu(root)
filemenu = tk.Menu(menubar, tearoff=0) #тироф это отделение окна
filemenu.add_command(label="Выбрать файл", command=load_video)
# filemenu.add_separator()
filemenu.add_command(label="Выход", command=root.quit)
menubar.add_cascade(label="Медиа", menu=filemenu)

# Меню "Помощь"
helpmenu = tk.Menu(menubar, tearoff=0)
helpmenu.add_command(label="Справка пользования", command=show_help)
menubar.add_cascade(label="Помощь", menu=helpmenu)

root.config(menu=menubar)

def create_playlist_window():
    """Окно управления плейлистом"""
    playlist_win = tk.Toplevel(root)
    playlist_win.title("Плейлист")

    tk.Label(playlist_win, text="Добавьте файлы").pack(pady=5)

    # Список файлов
    listbox = tk.Listbox(playlist_win, width=50)
    listbox.pack(pady=5)

    for item in playlist:
        listbox.insert(tk.END, item.split('/')[-1])

    def add_files():
        """Добавляет файлы в плейлист"""
        files = filedialog.askopenfilenames(filetypes=[("Video Files", "*.mp4 *.avi *.mkv")])
        if files:
            for file in files:
                if file not in playlist:
                    playlist.append(file)
                    listbox.insert(tk.END, file.split('/')[-1])

    def remove_file():
        """Удаляет выбранный файл"""
        selected = listbox.curselection()
        if selected:
            playlist.pop(selected[0])
            listbox.delete(selected[0])

    def save_playlist():
        """Сохраняет плейлист в файл"""
        file_path = filedialog.asksaveasfilename(defaultextension=".txt")
        if file_path:
            with open(file_path, 'w') as f:
                f.write('\n'.join(playlist))

    def load_playlist():
        """Загружает плейлист из файла"""
        file_path = filedialog.askopenfilename(filetypes=[("Playlist Files", "*.txt")])
        if file_path:
            with open(file_path, 'r') as f:
                playlist = [line.strip() for line in f.readlines()]
            listbox.delete(0, tk.END)
            for item in playlist:
                listbox.insert(tk.END, item.split('/')[-1])

    # Кнопки управления плейлистом
    btn_frame = tk.Frame(playlist_win)
    btn_frame.pack(pady=5)

    tk.Button(btn_frame, text="Добавить", command=add_files).pack(side=tk.LEFT, padx=5)
    tk.Button(btn_frame, text="Удалить", command=remove_file).pack(side=tk.LEFT, padx=5)
    tk.Button(btn_frame, text="Сохранить", command=save_playlist).pack(side=tk.LEFT, padx=5)
    tk.Button(btn_frame, text="Загрузить", command=load_playlist).pack(side=tk.LEFT, padx=5)

def play_next_video():
    """Воспроизводит следующее видео в плейлисте"""
    global current_video_index

    if not playlist:
        return

    if shuffle_mode:
        current_video_index = random.randint(0, len(playlist) - 1)
    else:
        current_video_index = (current_video_index + 1) % len(playlist)

    load_video(playlist[current_video_index])


def toggle_playlist():
    """Включает/выключает плейлист"""
    global playlist_active
    playlist_active = not playlist_active
    playlist_btn["text"] = "Выкл плейлист" if playlist_active else "Вкл плейлист"


def toggle_shuffle():
    """Включает/выключает случайный порядок"""
    global shuffle_mode
    shuffle_mode = not shuffle_mode
    shuffle_btn["text"] = "Случайный: ВКЛ" if shuffle_mode else "Случайный: ВЫКЛ"


def toggle_repeat():
    """Включает/выключает повтор одной дорожки"""
    global repeat_one_mode
    repeat_one_mode = not repeat_one_mode
    repeat_btn["text"] = "Повтор: ВКЛ" if repeat_one_mode else "Повтор: ВЫКЛ"

# Панель плейлиста
playlist_frame = tk.Frame(root)
playlist_frame.pack(anchor='s',fill='x', padx=5, pady=5)

playlist_btn = tk.Button(playlist_frame, text="Создать плейлист", command=create_playlist_window)
playlist_btn.pack(side=tk.LEFT, padx=5)

toggle_btn = tk.Button(playlist_frame, text="Вкл плейлист", command=toggle_playlist)
toggle_btn.pack(side=tk.LEFT, padx=5)

shuffle_btn = tk.Button(playlist_frame, text="Случайный: ВЫКЛ", command=toggle_shuffle)
shuffle_btn.pack(side=tk.LEFT, padx=5)

repeat_btn = tk.Button(playlist_frame, text="Повтор: ВЫКЛ", command=toggle_repeat)
repeat_btn.pack(side=tk.LEFT, padx=5)


# load_btn = tk.Button(root, text="Load", command=load_video)
# load_btn.pack()

vid_player = TkinterVideo(scaled=True, master=root,bg="black")
vid_player.pack(expand=True, fill="both",padx=5)

play_pause_btn = tk.Button(root, text="Play", command=play_pause)
play_pause_btn.pack(padx=5, pady=5, anchor='w')

skip_plus_5sec = tk.Button(root, text="Skip -5 sec", command=lambda: skip(-5))
skip_plus_5sec.pack(side="left")

start_time = tk.Label(root, text=str(datetime.timedelta(seconds=0)))
start_time.pack(side="left")

progress_value = tk.IntVar(root)

progress_slider = tk.Scale(root, variable=progress_value, from_=0, to=0, orient="horizontal", command=my_seek)
progress_slider.bind("<ButtonRelease-1>", my_seek)
progress_slider.pack(side="left", fill="x", expand=True)

end_time = tk.Label(root, text=str(datetime.timedelta(seconds=0)))
end_time.pack(side="left")

vid_player.bind("<<Duration>>", update_duration)
vid_player.bind("<<SecondChanged>>", update_scale)
vid_player.bind("<<Ended>>", video_ended )

skip_plus_5sec = tk.Button(root, text="Skip +5 sec", command=lambda: skip(5))
skip_plus_5sec.pack(side="left")

root.mainloop()