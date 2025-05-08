import tkinter as tk
from tkinter import filedialog, messagebox
from tkVideoPlayer import TkinterVideo

# Создаем главное окно
root = tk.Tk()
root.title("Простой видеоплеер")
root.geometry("800x600")

# Переменные
video_path = ""
is_playing = False

# Создаем видеоплеер
videoplayer = TkinterVideo(root, scaled=True)
videoplayer.pack(expand=True, fill="both")

# Функции
def open_file():
    global video_path
    file_path = filedialog.askopenfilename(filetypes=[("Video Files", "*.mp4 *.avi *.mkv")])
    if file_path:
        video_path = file_path
        videoplayer.load(file_path)
        play_video()

def play_video():
    global is_playing
    if video_path:
        if is_playing:
            videoplayer.pause()
            play_btn.config(text="Play")
            is_playing = False
        else:
            videoplayer.play()
            play_btn.config(text="Pause")
            is_playing = True

def stop_video():
    global is_playing
    videoplayer.stop()
    play_btn.config(text="Play")
    is_playing = False

def show_help():
    messagebox.showinfo("Помощь", "Простой видеоплеер\n\n"
                        "1. Нажмите 'Открыть' чтобы выбрать видео\n"
                        "2. Используйте кнопки Play/Pause и Stop\n"
                        "3. Перетаскивайте ползунок для перемотки")

# Меню
menubar = tk.Menu(root)
filemenu = tk.Menu(menubar, tearoff=0)
filemenu.add_command(label="Открыть", command=open_file)
filemenu.add_command(label="Выход", command=root.quit)
menubar.add_cascade(label="Файл", menu=filemenu)

helpmenu = tk.Menu(menubar, tearoff=0)
helpmenu.add_command(label="Помощь", command=show_help)
menubar.add_cascade(label="Справка", menu=helpmenu)

root.config(menu=menubar)

# Ползунок прогресса
progress = tk.Scale(root, from_=0, to=100, orient=tk.HORIZONTAL)
progress.pack(fill=tk.X, padx=10, pady=5)

# Кнопки управления
controls = tk.Frame(root)
controls.pack(pady=10)

play_btn = tk.Button(controls, text="Play", command=play_video)
play_btn.pack(side=tk.LEFT, padx=5)

stop_btn = tk.Button(controls, text="Stop", command=stop_video)
stop_btn.pack(side=tk.LEFT, padx=5)

# Обновление ползунка
def update_slider():
    if videoplayer.is_playing():
        current_time = videoplayer.current_duration()
        progress.set(current_time)
    root.after(100, update_slider)

def seek(value):
    videoplayer.seek(int(value))

progress.config(command=seek)
update_slider()

root.mainloop()