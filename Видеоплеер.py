import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import random
import itertools
import time
import vlc
import os

vlc_path = r"C:\Program Files\VideoLAN\VLC"
os.add_dll_directory(vlc_path)



def exit():
    player.stop()
    root.quit()

def open_help():
    help_text = "Инструкция по использованию приложения:\n\n"
    help_text += "1. Нажмите 'Выбрать видео', чтобы загрузить видеофайл.\n"
    help_text += "2. Используйте кнопку '⏸' для паузы/воспроизведения.\n"
    help_text += "3. Используйте кнопку 'Плейлист' для управления списком воспроизведения.\n"
    help_text += "4. Для выхода используйте кнопку 'Выход'.\n"
    messagebox.showinfo("Помощь", help_text)

def select_video():
    file_path = filedialog.askopenfilename(filetypes=[("Video files", "*.mp4 *.avi *.mov *.mkv")])
    if file_path:
        load_and_play(file_path)

def pause(): #pause
    if player.is_playing():
        player.pause()
        pause_btn.config(text="▶️")
    else:
        player.play()
        pause_btn.config(text="⏸️")

def update_playlist():
    if 'playlist_listbox' in globals():
        playlist_listbox.delete(0, tk.END)
        for i in playlist:
            playlist_listbox.insert(tk.END, i.split('/')[-1])

def load_and_play(file_path):
    player.stop()
    media = vlc_instance.media_new(file_path)
    player.set_media(media)
    set_player_ww()
    player.play()
    pause_btn.config(text="⏸️")
    time.sleep(0.1)

def set_player_ww():
    player.set_hwnd(video_frame.winfo_id())


def toggle_playlist_window(): #открывает/закрывает окно плейлиста
    global playlist_ww

    if playlist_ww and playlist_ww.winfo_exists():
        # Если окно существует - закрытие окна
        playlist_ww.destroy()
        playlist_ww = None
    else:
        # Создание новое окно плейлиста
        open_playlist_ww()

def open_playlist_ww(): #открытие плейлиста
    def del_vids(): #удаление выбранных видео в плейлисте
        selected = playlist_listbox.curselection()
        for i in reversed(selected):
            del playlist[i]
        update_playlist()

    def add_vids(): #добавление видео в плейлист
        files = filedialog.askopenfilenames(filetypes=[("Video files", "*.mp4 *.avi *.mov *.mkv")])
        if files:
            playlist.extend(files)
            update_playlist()

    def save_vids():  # сохранение плейлиста как текстового файла
        filepath = filedialog.asksaveasfilename(defaultextension='.txt', filetypes=[
            ("Text files", "*.txt")])  # deftxtnn это автоматическое задание расширения
        if filepath:
            try:
                with open(filepath, 'w',
                          encoding='utf-8') as output:  # контекст.менеджер; 1-путь к файлу, 2-режим открытия, 3-кодировка; c сохранением в пер-ю filepath
                    for i in playlist:
                        print(i, file=output)  # запись в файл
                messagebox.showinfo("Сохранено", 'Ваш плейлист сохранен')
            except:
                messagebox.showerror("Ошибка", "Не выбран путь для сохранения файла")

    def load_playlist(): #загрузка плейлиста из памяти компьютера как текстового файла
        file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        if file_path:
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    loaded_paths = [line.strip() for line in f.readlines() if line.strip()]
                    playlist.clear()
                    playlist.extend(loaded_paths)
                    update_playlist()
                messagebox.showinfo("Успешно", "Плейлист загружен.")
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось загрузить плейлист:\n{e}")

    def play_some(index): #для кнопки 'воспроизвести' в окне плейлиста
        if 0 <= index and index < len(playlist):
            file_path = playlist[index]
            load_and_play(file_path)

    def play_selected(): #если видео выбрано, проигрывание начинается с выбранного видео
        if not playlist:
            messagebox.showinfo("Плейлист пуст", "Сначала добавьте видео в плейлист.")
            return
        selected = playlist_listbox.curselection()
        if selected:
            start_index = selected[0]  # индекс выбранного видео в плейлисте
        else:
            start_index = 0

        def play_next(index): #запуск след. видео в плейлисте
            if 0 <= index < len(playlist):
                play_some(index)
            else:
                play_some(0)


        def check_video_end(): #проверка окончания видео
            nonlocal start_index
            if player.get_length() > 0:
                if player.get_state() == vlc.State.Ended:
                    if playlist_auto:
                        next_index = (start_index + 1) % len(playlist)
                        start_index = next_index
                        play_next(next_index)
            root.after(1000, check_video_end)

        play_next(start_index)
        root.after(1000, check_video_end)


    global playlist_ww
    playlist_ww = tk.Toplevel(master=root,bg='darkolivegreen')
    playlist_ww.title("Плейлист")
    playlist_ww.geometry("400x300")

    global playlist_listbox
    playlist_listbox = tk.Listbox(master=playlist_ww,bg='darkolivegreen')
    playlist_listbox.pack(fill="both", expand=True, padx=10, pady=10)

    btn_frame = tk.Frame(master=playlist_ww, bg='darkolivegreen')
    btn_frame.pack(pady=5)

    add_btn = tk.Button(master=btn_frame, text="Добавить", command=add_vids)
    add_btn.grid(row=0, column=0, padx=5)

    del_btn = tk.Button(master=btn_frame, text="Удалить", command=del_vids)
    del_btn.grid(row=0, column=1, padx=5)

    save_btn = tk.Button(master=btn_frame, text="Сохранить", command=save_vids)
    save_btn.grid(row=0, column=2, padx=5)

    load_btn = tk.Button(master=btn_frame, text="Загрузить", command=load_playlist)
    load_btn.grid(row=0, column=3, padx=5)

    play_btn = tk.Button(master=btn_frame, text="Воспроизвести", command=play_selected)
    play_btn.grid(row=0, column=4, padx=5)

    update_playlist()

def format_time(ms):
    if ms is None or ms < 0:
        return "00:00"
    else:
        seconds = ms // 1000
        if seconds < 3600:
            mins = int(seconds // 60)
            secs = int(seconds % 60)
            return f'{mins:02d}:{secs:02d}'  # 02d -форматир-е
        else:
            hours = int(seconds // 3600)
            mins = int((seconds - 3600 * hours) // 60)
            secs = int((seconds - 3600 * hours) % 60)
            return f'{hours:02d}{mins:02d}:{secs:02d}'

def upd_slider():
    if player.get_length() > 0:
        length = player.get_length()
        current = player.get_time()
        slider.config(to=100)
        slider.set(current * 100 / length)
        curr_time.config(text=format_time(current))
        dur_time.config(text=format_time(length))
    else:
        curr_time.config(text="00:00")
        dur_time.config(text="00:00")

    root.after(500, upd_slider)


def slider_change(event):
    if player.get_length()>0:
        current_time = int(slider.get()*player.get_length()/100)
        player.set_time(current_time)

def play_random():
    global shuffled_iterator
    if not playlist:
        messagebox.showinfo("Ошибка","Плейлист пуст")
        return

    shuffled = playlist.copy()
    random.shuffle(shuffled)
    shuffled_iterator = itertools.cycle(shuffled)

    def play_next_random():
        path = next(shuffled_iterator)
        load_and_play(path)

    def check_video_end():
        if player.get_length() > 0:
            if player.get_state() == vlc.State.Ended:
                play_next_random()
        root.after(1000, check_video_end)

    play_next_random()
    root.after(1000, check_video_end)



def repeat():
    global repeat_current
    repeat_current = not repeat_current
    repeat_btn.config(relief=tk.SUNKEN if repeat_current else tk.RAISED)

def playlist_mod():
    global playlist_auto
    playlist_auto = not playlist_auto
    if playlist:
        enable_playlist_btn.config(text="Откл. плейлист" if playlist_auto else "Вкл. плейлист")
    else:
        messagebox.showinfo('Ошибка', 'Плейлист не создан')


def setup_vlc_events():
    event_manager = player.event_manager()
    event_manager.event_attach(vlc.EventType.MediaPlayerEndReached, on_end_reached)

def on_end_reached(event):
    if repeat_current:
        root.after(100, restart_video)

def restart_video():
    try:
        player.stop()
        player.set_time(0)
        player.play()
    except Exception as e:
        print(f"Ошибка при перезапуске видео: {e}")
        messagebox.showerror("Ошибка", f"Не удалось перезапустить видео: {e}")

def volume_change(val):
    volume = int(float(val))
    player.audio_set_volume(volume)


root = tk.Tk()
root.title('Видеоплеер')
root.iconbitmap(default="illustration2.ico")
root.geometry("1000x600+170-100")
root.configure(bg='darkolivegreen')
root.minsize(800,600)

playlist = []
playlist_auto = True #сигнализатор нажатия кнопки
repeat_current = False
playlist_ww = None  # Для отслеживания окна плейлиста

video_frame = tk.Frame(root, bg="black")
video_frame.pack(expand=True, fill="both")

vlc_instance = vlc.Instance()
player = vlc_instance.media_player_new()
setup_vlc_events()
player.audio_set_volume(80)

# Ползунок и время
slider_frame = tk.Frame(master=root,bg='darkolivegreen')
slider_frame.pack(pady=10)

curr_time = tk.Label(slider_frame, text="00:00", width=5, font=("Arial", 10),bg='darkolivegreen')
curr_time.pack(side=tk.LEFT, padx=5)

slider = tk.Scale(slider_frame, from_=0, to=100, orient="horizontal", length=600, sliderlength=20, showvalue=False,bg='darkolivegreen')
slider.pack(side=tk.LEFT, padx=5)
slider.bind("<ButtonRelease-1>", slider_change)

dur_time = tk.Label(slider_frame, text="00:00", width=5, font=("Arial", 10),bg='darkolivegreen')
dur_time.pack(side=tk.LEFT, padx=5)


btn_frame = tk.Frame(master=root,bg='darkolivegreen')
btn_frame.pack(pady=10)

pause_btn = tk.Button(btn_frame, text="⏸️", command=pause)
pause_btn.grid(row=0, column=1, padx=5)

playlist_btn = tk.Button(btn_frame, text="Плейлист", command=toggle_playlist_window)
playlist_btn.grid(row=0, column=3, padx=5)

random_btn = tk.Button(btn_frame, text="Случайный порядок", command=play_random)
random_btn.grid(row=0, column=5, padx=5)

repeat_btn = tk.Button(btn_frame, text="Повтор 1 дорожки", command=repeat)
repeat_btn.grid(row=0, column=6, padx=5)

enable_playlist_btn = tk.Button(btn_frame, text="Откл. плейлист", command=playlist_mod)
enable_playlist_btn.grid(row=0, column=4, padx=5)

volume_slider = tk.Scale(master=slider_frame,from_=100,to=0,orient="vertical",length=50, sliderlength=10, command=volume_change,bg='darkolivegreen')
volume_slider.set(80) #автом-ки громкость =80
volume_slider.pack(side=tk.RIGHT,padx=5)

menubar = tk.Menu(master=root)

media_menu = tk.Menu(master=menubar, tearoff=0)
media_menu.add_command(label="Выбрать файл",command=select_video)
media_menu.add_command(label='Выход',command=exit)

help_menu = tk.Menu(master=menubar,tearoff=0)
help_menu.add_command(label='Справка пользования',command=open_help)

menubar.add_cascade(label='Медиа',menu=media_menu)
menubar.add_cascade(label='Помощь',menu=help_menu)

root.config(menu=menubar)

upd_slider()

root.mainloop()