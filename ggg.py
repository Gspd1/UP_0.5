import os
import random
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from tkVideoPlayer import TkinterVideo


class VideoPlayerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Видеоплеер")
        self.root.geometry("800x600")

        # Переменные для плейлиста
        self.playlist = []
        self.current_video_index = 0
        self.playlist_enabled = False
        self.random_order = False
        self.repeat_one = False

        # Создание интерфейса
        self.create_menu()
        self.create_video_player()
        self.create_progress_bar()
        self.create_playlist_controls()

    def create_menu(self):
        # Меню "Медиа"
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)

        media_menu = tk.Menu(menubar, tearoff=0)
        media_menu.add_command(label="Выбрать файл", command=self.open_file)
        media_menu.add_command(label="Выход", command=self.root.quit)
        menubar.add_cascade(label="Медиа", menu=media_menu)

        # Кнопка "Помощь"
        help_menu = tk.Menu(menubar, tearoff=0)
        help_menu.add_command(label="Справка", command=self.show_help)
        menubar.add_cascade(label="Помощь", menu=help_menu)

    def create_video_player(self):
        # Область воспроизведения видео
        self.video_frame = tk.Frame(self.root, bg='black')
        self.video_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.videoplayer = TkinterVideo(self.video_frame, scaled=True)
        self.videoplayer.pack(fill=tk.BOTH, expand=True)

        # Кнопки управления
        control_frame = tk.Frame(self.root)
        control_frame.pack(pady=5)

        self.play_btn = tk.Button(control_frame, text="Play", command=self.play_video)
        self.play_btn.pack(side=tk.LEFT, padx=5)

        self.stop_btn = tk.Button(control_frame, text="Stop", command=self.stop_video)
        self.stop_btn.pack(side=tk.LEFT, padx=5)

    def create_progress_bar(self):
        # Прогрессбар
        self.progress_frame = tk.Frame(self.root)
        self.progress_frame.pack(fill=tk.X, padx=10, pady=5)

        self.progress = ttk.Progressbar(
            self.progress_frame,
            orient=tk.HORIZONTAL,
            mode='determinate'
        )
        self.progress.pack(fill=tk.X)

        self.videoplayer.bind("<<Duration>>", self.update_duration)
        self.videoplayer.bind("<<SecondChanged>>", self.update_scale)

    def create_playlist_controls(self):
        # Кнопки управления плейлистом
        playlist_frame = tk.Frame(self.root)
        playlist_frame.pack(fill=tk.X, padx=10, pady=5)

        self.create_playlist_btn = tk.Button(
            playlist_frame,
            text="Создать плейлист",
            command=self.open_playlist_window
        )
        self.create_playlist_btn.pack(side=tk.LEFT, padx=5)

        self.toggle_playlist_btn = tk.Button(
            playlist_frame,
            text="Вкл/Выкл плейлист",
            command=self.toggle_playlist
        )
        self.toggle_playlist_btn.pack(side=tk.LEFT, padx=5)

        self.random_order_btn = tk.Button(
            playlist_frame,
            text="Случайный порядок",
            command=self.toggle_random_order
        )
        self.random_order_btn.pack(side=tk.LEFT, padx=5)

        self.repeat_one_btn = tk.Button(
            playlist_frame,
            text="Повтор 1 дорожки",
            command=self.toggle_repeat_one
        )
        self.repeat_one_btn.pack(side=tk.LEFT, padx=5)

    def open_playlist_window(self):
        playlist_window = tk.Toplevel(self.root)
        playlist_window.title("Редактор плейлиста")
        playlist_window.geometry("500x400")

        # Область для перетаскивания файлов
        drop_frame = tk.LabelFrame(playlist_window, text="Перетащите файлы сюда")
        drop_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        drop_label = tk.Label(drop_frame, text="Перетащите видеофайлы сюда")
        drop_label.pack(expand=True)

        # Кнопки управления плейлистом
        btn_frame = tk.Frame(playlist_window)
        btn_frame.pack(fill=tk.X, padx=10, pady=5)

        save_btn = tk.Button(
            btn_frame,
            text="Сохранить",
            command=lambda: self.save_playlist(playlist_window)
        )
        save_btn.pack(side=tk.LEFT, padx=5)

        open_btn = tk.Button(
            btn_frame,
            text="Открыть",
            command=self.load_playlist
        )
        open_btn.pack(side=tk.LEFT, padx=5)

        # Привязка событий перетаскивания
        drop_frame.drop_target_register(tk.DND_FILES)
        drop_frame.dnd_bind('<<Drop>>', lambda e: self.add_files_to_playlist(e.data, drop_label))

    def add_files_to_playlist(self, files, label):
        file_list = self.root.tk.splitlist(files)
        self.playlist = [f for f in file_list if f.lower().endswith(('.mp4', '.avi', '.mov', '.mkv'))]
        label.config(text=f"Добавлено {len(self.playlist)} файлов")

    def save_playlist(self, window):
        if not self.playlist:
            messagebox.showwarning("Ошибка", "Плейлист пуст!")
            return

        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Текстовые файлы", "*.txt")]
        )

        if file_path:
            with open(file_path, 'w') as f:
                f.write('\n'.join(self.playlist))
            window.destroy()

    def load_playlist(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("Текстовые файлы", "*.txt")]
        )

        if file_path:
            with open(file_path, 'r') as f:
                self.playlist = [line.strip() for line in f.readlines() if os.path.exists(line.strip())]

            if self.playlist:
                messagebox.showinfo("Успех", f"Загружен плейлист из {len(self.playlist)} файлов")
            else:
                messagebox.showwarning("Ошибка", "Не удалось загрузить плейлист")

    def toggle_playlist(self):
        self.playlist_enabled = not self.playlist_enabled
        if self.playlist_enabled and self.playlist:
            self.play_next_video()

    def toggle_random_order(self):
        self.random_order = not self.random_order
        if self.random_order:
            self.repeat_one = False

    def toggle_repeat_one(self):
        self.repeat_one = not self.repeat_one
        if self.repeat_one:
            self.random_order = False

    def play_next_video(self):
        if not self.playlist or not self.playlist_enabled:
            return

        if self.repeat_one:
            pass  # Просто продолжаем воспроизводить текущее видео
        elif self.random_order:
            self.current_video_index = random.randint(0, len(self.playlist) - 1)
        else:
            self.current_video_index = (self.current_video_index + 1) % len(self.playlist)

        self.play_video_file(self.playlist[self.current_video_index])

    def play_video_file(self, file_path):
        self.videoplayer.load(file_path)
        self.videoplayer.play()
        self.play_btn.config(text="Pause", command=self.pause_video)

    def play_video(self):
        if self.videoplayer.is_paused():
            self.videoplayer.play()
            self.play_btn.config(text="Pause", command=self.pause_video)
        else:
            if not self.playlist_enabled:
                file_path = filedialog.askopenfilename(filetypes=[
                    ("Видео файлы", "*.mp4 *.avi *.mov *.mkv")
                ])
                if file_path:
                    self.play_video_file(file_path)
            else:
                self.play_next_video()

    def pause_video(self):
        self.videoplayer.pause()
        self.play_btn.config(text="Play", command=self.play_video)

    def stop_video(self):
        self.videoplayer.stop()
        self.play_btn.config(text="Play", command=self.play_video)

    def update_duration(self, event):
        duration = self.videoplayer.video_info()["duration"]
        self.progress["maximum"] = duration

    def update_scale(self, event):
        current_time = self.videoplayer.current_duration()
        self.progress["value"] = current_time

        # Проверка окончания видео для плейлиста
        if current_time >= self.progress["maximum"] and self.playlist_enabled:
            self.play_next_video()

    def show_help(self):
        help_text = """Справка пользования:
1. Используйте кнопки Play/Pause и Stop для управления воспроизведением
2. В меню 'Медиа' можно выбрать файл или выйти из программы
3. Для работы с плейлистом:
   - Создайте плейлист, перетащив файлы в окно редактора
   - Сохраните/загрузите плейлист
   - Используйте кнопки управления плейлистом"""

        messagebox.showinfo("Справка", help_text)

    def open_file(self):
        file_path = filedialog.askopenfilename(filetypes=[
            ("Видео файлы", "*.mp4 *.avi *.mov *.mkv")
        ])
        if file_path:
            self.play_video_file(file_path)


if __name__ == "__main__":
    root = tk.Tk()
    app = VideoPlayerApp(root)
    root.mainloop()