import tkinter as tk
from tkinter import filedialog, messagebox
from tkVideoPlayer import TkinterVideo


def main():
    root = tk.Tk()
    root.title("Мой Видеоплеер")
    root.geometry("800x600")


    video_player = TkinterVideo(root, scaled=True)
    video_player.pack(expand=True, fill="both", padx=10, pady=10)


    current_video = ""
    is_playing = False


    def play_pause():
        nonlocal is_playing
        if current_video:
            if is_playing:
                video_player.pause()
                play_btn.config(text="▶️ Играть")
            else:
                video_player.play()
                play_btn.config(text="⏸️ Пауза")
            is_playing = not is_playing

    def stop_video():
        nonlocal is_playing
        video_player.stop()
        play_btn.config(text="▶️ Играть")
        is_playing = False
        progress_slider.set(0)

    def open_file():
        nonlocal current_video
        file = filedialog.askopenfilename(
            filetypes=[("Видео файлы", "*.mp4 *.avi *.mkv *.mov"), ("Все файлы", "*.*")]
        )
        if file:
            current_video = file
            video_player.load(file)
            progress_slider.config(to=0, from_=0)
            play_pause()

    def update_progress():
        if video_player.is_paused():
            current_time = video_player.current_duration()
            progress_slider.set(current_time)
        root.after(100, update_progress)

    def seek_video(value):
        video_player.seek(int(float(value)))

    def show_help():
        help_text = """Справка по видеоплееру:

1. Открыть - выбрать видеофайл
2. ▶️ Играть/⏸️ Пауза - управление воспроизведением
3. ⏹️ Стоп - остановить видео
4. Ползунок - перемотка видео
5. 🔈 Громкость - регулировка звука"""
        messagebox.showinfo("Помощь", help_text)


    menubar = tk.Menu(root)

    file_menu = tk.Menu(menubar, tearoff=0)
    file_menu.add_command(label="Открыть", command=open_file)
    file_menu.add_separator()
    file_menu.add_command(label="Выход", command=root.quit)
    menubar.add_cascade(label="Файл", menu=file_menu)

    help_menu = tk.Menu(menubar, tearoff=0)
    help_menu.add_command(label="Справка", command=show_help)
    menubar.add_cascade(label="Помощь", menu=help_menu)

    root.config(menu=menubar)


    control_frame = tk.Frame(root)
    control_frame.pack(fill="x", padx=10, pady=5)


    play_btn = tk.Button(control_frame, text="▶️ Играть", command=play_pause)
    play_btn.pack(side="left", padx=5)

    stop_btn = tk.Button(control_frame, text="⏹️ Стоп", command=stop_video)
    stop_btn.pack(side="left", padx=5)


    progress_slider = tk.Scale(root, from_=0, to=100, orient="horizontal")
    progress_slider.pack(fill="x", padx=10, pady=5)
    progress_slider.config(command=seek_video)

    
    update_progress()

    root.mainloop()


if __name__ == "__main__":
    main()
