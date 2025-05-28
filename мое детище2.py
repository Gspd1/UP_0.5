import tkinter as tk
from tkVideoPlayer import TkinterVideo
from tkinter import messagebox
from tkinter import filedialog
import itertools

playlist = []


def exit():
    root.quit()

def open_help():
    help_text = "Пробник"
    messagebox.showinfo('Помощь', help_text)

def select_video():
    file_path = filedialog.askopenfilename(filetypes=[('video files', '*.mp4 *.avi *.mov *.mkv')])
    if file_path:
        videoplayer.stop()
        videoplayer.load(file_path)
        videoplayer.play()

def pause():
    if videoplayer.is_paused():
        videoplayer.play()
        pause_btn.config(text="▶️")
    else:
        videoplayer.pause()
        pause_btn.config(text='⏸️')



def fullscr():
    a = root.attributes('-fullscreen')
    if a:
        root.attributes('-fullscreen',False)
        fullscreen_btn.config(text='Fullscreen')
    else:
        root.attributes('-fullscreen',True)
        fullscreen_btn.config(text='Lowscreen')

def update_playlist():
    if 'playlist_listbox' in globals():
        playlist_listbox.delete(0, tk.END)
        for i in playlist:
            playlist_listbox.insert(tk.END, i.split('/')[-1])

def open_playlist_ww():

    def del_vids():
        selected = playlist_listbox.curselection()  #индексы выбр. мышкой видео
        for i in selected:
            del playlist[i] #удаляет видео по тому индексу который вставим
        update_playlist()

    def add_vids():
        files = filedialog.askopenfilenames(filetypes=[("Video files", "*.mp4 *.avi *.mov *.mkv")])
        if files:
            playlist.extend(files)
            update_playlist()

    def save_vids():
        with open('save.txt','w',encoding='utf-8') as output: #контекст.менеджер; 1-путь к файлу, 2-режим открытия, 3-кодировка; c сохранением в пер-ю file
            for i in playlist:
                print(i,file=output) #запись в файл
        messagebox.showinfo("Сохранено", 'Ваш плейлист сохранен')

    def load_playlist():
        file = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        if file:
            try:
                with open(file,'r',encoding='utf-8') as f: #просто перем-я
                    path = [i.strip() for i in f.readlines()]
                    playlist.clear()
                    playlist.extend(path) #добавление
                    update_playlist()
            except:
                messagebox.showerror('Ошибка','Не удалось загрузить плейлист')

    def play_some(index):
        if 0<=index and index<len(playlist):
            filepath = playlist[index] #путь к необх.видео
            try:
                videoplayer.pause()
            except:
                pass

            def time_after_selection():
                try:
                    videoplayer.load(filepath)
                    videoplayer.play()
                    pause_btn.config(text="⏸️")
                except:
                    messagebox.showerror('Ошибка','Не удалось воспроизвести видео')

            root.after(400, time_after_selection)

    def play_selected():
        selected = playlist_listbox.curselection()
        if selected:
            play_some(selected[0])
        else:
            playlist_iterator = itertools.cycle(playlist) #воспр-е с 1го видео с пом-ю итерации

            def play_next():
                filepath = next(playlist_iterator)
                try:
                    videoplayer.stop()
                    videoplayer.load(filepath)
                    videoplayer.play()
                    pause_btn.config(text='⏸️')
                except Exception as e: #ошибка сохр-ся в пер-й 'е'
                    messagebox.showerror('Ошибка',f'Не удалось воспроизвести видео\n{e}')

            def check_vid():
                duration = videoplayer.video_info()['duration']
                current = videoplayer.current_duration()
                if int(current)>=int(duration):
                    play_next()
                root.after(500,check_vid) #задержка в мс, вызов ф-и check_vid
            play_next()
            check_vid()





    playlist_ww = tk.Toplevel(master=root)
    playlist_ww.title('Плейлист')
    playlist_ww.geometry('400x300')

    global playlist_listbox
    playlist_listbox = tk.Listbox(master=playlist_ww)
    playlist_listbox.pack(fill='both',expand=True,padx=10,pady=10)
    btn_frame = tk.Frame(master=playlist_ww)
    btn_frame.pack(pady=5)

    add_btn = tk.Button(master=btn_frame,text="Добавить",command=add_vids)
    add_btn.grid(row=0,column=0,padx=5)

    del_btn = tk.Button(master=btn_frame,text="Удалить",command=del_vids)
    del_btn.grid(row=0, column=1, padx=5)

    save_btn = tk.Button(master=btn_frame,text="Сохранить",command=save_vids)
    save_btn.grid(row=0, column=2, padx=5)

    load_btn = tk.Button(master=btn_frame,text="Загрузить",command=load_playlist)
    load_btn.grid(row=0, column=3, padx=5)

    play_btn = tk.Button(master=btn_frame,text="Воспроизвести", command=play_selected)
    play_btn.grid(row=0, column=4, padx=5)

    update_playlist()

def format_time(seconds):
    if seconds is None or seconds<0:
        return '00:00'
    else:
        if seconds<3600:
            mins = int(seconds//60)
            secs = int(seconds % 60)
            return f'{mins:02d}:{secs:02d}' #02d -форматир-е
        else:
            hours = int(seconds//3600)
            mins = int((seconds-3600*hours)//60)
            secs = int((seconds-3600*hours)%60)
            return f'{hours:02d}{mins:02d}:{secs:02d}'

def upd_slider():
    if videoplayer and videoplayer.video_info():
        duration = videoplayer.video_info().get('duration',0)
        current = videoplayer.current_duration()
        slider.config(to=int(duration))
        slider.set(int(current))
        curr_time.config(text=format_time(current))
        dur_time.config(text=format_time(duration))
    root.after(10,upd_slider)

def slider_change(event):
    current_time = slider.get()
    videoplayer.seek(current_time)   #НАПИСАТЬ Ф-Ю АПД_СЛАЙДЕР


root = tk.Tk()
root.title('Видеоплеер')
root.geometry('800x600')

videoframe = tk.Frame(root, bg='black')
videoframe.pack(fill='both',expand=True)


videoplayer = TkinterVideo(master=videoframe,scaled=True)
videoplayer.pack(fill='both',expand=True)


slider_frame = tk.Frame(master=root)
slider_frame.pack(pady=10)

curr_time = tk.Label(master=slider_frame,text='00:00',font=('Arial',10))
curr_time.pack(side=tk.LEFT,padx=5)

slider = tk.Scale(master=slider_frame,from_=0,to=100,orient='horizontal',length=600,sliderlength=20,showvalue=False)
slider.pack(side=tk.LEFT,padx=5)
slider.bind("<ButtonRelease-1>",slider_change) #<ButtonRelease-1> -ивент

dur_time = tk.Label(master=slider_frame,text='00:00',font=('Arial',10))
dur_time.pack(side=tk.LEFT,padx=5)


btn_frame = tk.Frame(master=root)
btn_frame.pack(pady=10)

pause_btn = tk.Button(master=btn_frame,text='⏸️',command=pause)
pause_btn.grid(row=0,column=1,padx=5)

fullscreen_btn = tk.Button(master=btn_frame,text='Fullscreen',command=fullscr)
fullscreen_btn.grid(row=0,column=2, padx=5)

playlist_btn = tk.Button(master=btn_frame, text='Плейлист',command=open_playlist_ww)
playlist_btn.grid(row=0,column=3, padx=5)



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