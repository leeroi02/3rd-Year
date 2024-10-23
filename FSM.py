import tkinter as tk
from tkinter import PhotoImage, ttk
import pygame
import os

script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)

# Finite State Machine Transition Table
transition_table = {
    'stop': {'play': 'play', 'next': 'play', 'back': 'play', 'pause': 'stop'},
    'play': {'pause': 'pause', 'stop': 'stop', 'next': 'play', 'back': 'play'},
    'pause': {'play': 'play', 'stop': 'stop', 'next': 'play', 'back': 'play'},
}

class MusicPlayerFSM:
    def __init__(self, root):
        self.state = 'stop'
        self.current_song = 0
        
        pygame.mixer.init()

        self.songs = [
            {
                'file': 'song1.mp3',
                'title': 'Juno',
                'singer': 'Sabrina Carpenter',
                'album_image': 'sabrina.png'
            },
            {
                'file': 'song2.mp3',
                'title': 'APT',
                'singer': 'Rose ft. Bruno Mars',
                'album_image': 'apt.png'
            },
            {
                'file': 'song3.mp3',
                'title': 'Gocha',
                'singer': 'Rick Astley',
                'album_image': 'gacha.png'
            }
        ]

        self.root = root
        self.root.title("Finite State Machine Player")
        self.root.geometry("600x600")
        self.root.config(bg="#f0f0f0")

        self.header_font = ("Arial", 14, "bold")
        self.font_style = ("Arial", 12)

        
        parent_frame = tk.Frame(self.root, bg="#f0f0f0")
        parent_frame.pack(pady=10)
        
        self.song_list_frame = tk.Frame(parent_frame, bg="#f0f0f0")
        self.song_list_frame.pack(pady=10, fill='both', expand=True, anchor='center')

        self.time_frame = tk.Frame(parent_frame, bg="#f0f0f0")
        self.time_frame.pack(pady=5, anchor='center')

        self.current_time_label = tk.Label(self.time_frame, text="0:00", font=self.font_style, bg="#f0f0f0")
        self.current_time_label.grid(row=0, column=0, padx=5)

        self.song_slider = ttk.Scale(self.time_frame, from_=0, to=100, orient='horizontal', length=400)
        self.song_slider.grid(row=0, column=1, padx=10)

        self.total_time_label = tk.Label(self.time_frame, text="0:00", font=self.font_style, bg="#f0f0f0")
        self.total_time_label.grid(row=0, column=2, padx=5)

        self.update_slider()

        # Control buttons 
        control_frame = tk.Frame(self.root, bg="#f0f0f0")
        control_frame.pack(pady=20)

        self.play_icon = tk.PhotoImage(file="play.png").subsample(10, 10)
        self.pause_icon = tk.PhotoImage(file="pause.png").subsample(10,10)
        self.stop_icon = tk.PhotoImage(file="stop.png").subsample(10,10)
        self.back_icon = tk.PhotoImage(file="back.png").subsample(10,10)
        self.next_icon = tk.PhotoImage(file="next.png").subsample(10,10)

        self.play_button = tk.Button(control_frame, image=self.play_icon, command=self.play)
        self.play_button.grid(row=0, column=1, padx=5, pady=5)

        self.pause_button = tk.Button(control_frame, image=self.pause_icon, command=self.pause, bg="#FFFFFF")
        self.pause_button.grid(row=0, column=2, padx=5, pady=5)

        self.stop_button = tk.Button(control_frame, image=self.stop_icon, command=self.stop, bg="#FFFFFF")
        self.stop_button.grid(row=0, column=3, padx=5, pady=5)

        self.back_button = tk.Button(control_frame, image=self.back_icon, command=self.back_song, bg="#FFFFFF")
        self.back_button.grid(row=0, column=0, padx=5, pady=5)

        self.next_button = tk.Button(control_frame, image=self.next_icon, command=self.next_song, bg="#FFFFFF")
        self.next_button.grid(row=0, column=4, padx=5, pady=5)

        self.state_label = tk.Label(self.root, font=self.header_font)
        self.state_label.pack(pady=10)

        self.state_label.config(text=f"State: {self.state}")
        
        button_frame = tk.Frame(root)
        button_frame.pack(side='bottom', anchor='sw', padx=10, pady=10)

        redirect_button = tk.Button(button_frame, text="View DFA", command=open_new_window)
        redirect_button.pack(side='right')

        # DFA Visualizer
        self.state_visualizer_frame = tk.Frame(self.root)
        self.state_visualizer_frame.pack(pady=20)

        self.state_labels = {}
        for idx, state in enumerate(transition_table.keys()):
            label = tk.Label(self.state_visualizer_frame, text=state, font=self.font_style, width=10)
            label.grid(row=0, column=idx, padx=5)
            self.state_labels[state] = label

        self.highlight_current_state()
        self.check_song_completion()
        self.display_song_list()

    def highlight_current_state(self):
        for state, label in self.state_labels.items():
            if state == self.state:
                label.config(bg="#ff99cc")
            else:
                label.config(bg="#D8BFD8")

    def transition(self, action):
        if action in transition_table[self.state]:
            self.state = transition_table[self.state][action]
            self.state_label.config(text=f"State: {self.state}")
            self.highlight_current_state()
        else:
            print(f"Cannot transition from {self.state} to {action}")

    def play(self):
        if self.state == 'pause':  
            pygame.mixer.music.unpause()
            self.transition('play')
        else:
            song_file = self.songs[self.current_song]['file']
            self.transition('play')
            pygame.mixer.music.load(song_file)
            pygame.mixer.music.play()
            self.display_song_list()  

    def pause(self):
        if self.state == 'play':  
            pygame.mixer.music.pause()
            self.transition('pause')

    def stop(self):
        self.transition('stop')
        pygame.mixer.music.stop()

    def next_song(self):
        self.current_song = (self.current_song + 1) % len(self.songs)
        song_file = self.songs[self.current_song]['file']
        pygame.mixer.music.load(song_file)
        pygame.mixer.music.play()
        self.transition('play')
        self.display_song_list()  

    def back_song(self):
        self.current_song = (self.current_song - 1) % len(self.songs)
        song_file = self.songs[self.current_song]['file']
        pygame.mixer.music.load(song_file)
        pygame.mixer.music.play()
        self.transition('play')
        self.display_song_list()  

    def check_song_completion(self):
        if self.state == 'play' and not pygame.mixer.music.get_busy():
            self.next_song()
        self.root.after(1000, self.check_song_completion)

    def display_song_list(self):
        for widget in self.song_list_frame.winfo_children():
            widget.destroy()
        current_song = self.songs[self.current_song]
        song_frame = tk.Frame(self.song_list_frame, bg="#f0f0f0", pady=10)
        song_frame.pack(fill='x')

        try:
            album_image = PhotoImage(file=current_song['album_image']).subsample(5, 5)  
        except Exception as e:
            print(f"Error loading image {current_song['album_image']}: {e}")
            album_image = None

        if album_image:
            image_label = tk.Label(song_frame, image=album_image, bg="#f0f0f0")
            image_label.image = album_image 
            image_label.pack(side='left', padx=10)
        else:
            image_label = tk.Label(song_frame, text="No Image", bg="#f0f0f0")
            image_label.pack(side='left', padx=10)

        details_frame = tk.Frame(song_frame, bg="#f0f0f0")
        details_frame.pack(side='left')

        title_label = tk.Label(details_frame, text=current_song['title'], font=("Arial", 12, "bold"), bg="#f0f0f0")
        title_label.pack(anchor='w')
        singer_label = tk.Label(details_frame, text=current_song['singer'], font=("Arial", 10), bg="#f0f0f0")
        singer_label.pack(anchor='w')

    def update_slider(self):
        if self.state == 'play':
            current_pos = pygame.mixer.music.get_pos() // 1000 
            if self.current_song == 0:
                song_length=206
            elif self.current_song == 1:
                song_length=170
            else:
                song_length=212

            self.song_slider.config(to=song_length)  
            self.song_slider.set(current_pos)
            self.current_time_label.config(text=f"{current_pos // 60}:{current_pos % 60:02d}")

            total_minutes, total_seconds = divmod(song_length, 60)
            self.total_time_label.config(text=f"{total_minutes}:{total_seconds:02d}")

        self.root.after(500, self.update_slider)

def open_new_window():
    
    new_window = tk.Toplevel(root)
    new_window.title("New Window with Image Background")
    new_window.geometry("800x800")
    
    try:
        bg_image = PhotoImage(file="dfa.png")  
        bg_label = tk.Label(new_window, image=bg_image)
        bg_label.image = bg_image  
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)  
    except Exception as e:
        print(f"Error loading image: {e}")

root = tk.Tk()
player = MusicPlayerFSM(root)
root.mainloop()
