import tkinter as tk
import lyricsgenius
import sys
import re
import threading
import os
import csv
from tkinter import scrolledtext, ttk

# Create the Genius API client
genius = lyricsgenius.Genius('YOUR_GENIUS_API_TOKEN_HERE')

# Redirect print statements to the status_text widget
class Redirect:
    def __init__(self, widget):
        self.widget = widget

    def write(self, string):
        self.widget.configure(state="normal")
        self.widget.insert(tk.END, string)
        self.widget.see(tk.END)
        self.widget.configure(state="disabled")
        sys.__stdout__.write(string)

    def flush(self):
        pass

# Helper function to format lyrics
def format_lyrics(song):
    lyrics = song.lyrics
    song_title = song.title
    song_artist = song.artist

    # Clean and format the lyrics
    lyrics = re.sub(r'\d*Embed$', '', lyrics).strip()
    # Normalize newlines: Ensure there are exactly two newlines before each "[" that does not already follow two newlines
    lyrics = re.sub(r'(?<!\n)\n?\[', '\n\n[', lyrics)
    lyrics = re.sub(r'\n{3,}', '\n\n', lyrics)

    # Ensure there is a newline before the first "["
    lyrics = re.sub(r'^(?!\n\n)(\[)', r'\n\n\1', lyrics, count=1)

    # Remove header text up to "Song Title Lyrics"
    header_pattern = re.compile(r'.*?' + re.escape(song_title) + r'\sLyrics', re.DOTALL)
    lyrics = header_pattern.sub('', lyrics).strip()

    # Remove "Genius Romanizations" if present
    if "Genius Romanizations" in song_artist:
        new_title = re.split(r'-', song_title)[0]
        song_artist = new_title
        pattern = re.escape(new_title) + r'\s*-\s*'
        song_title = re.sub(pattern, '', song_title)

    formatted_lyrics = f"{song_title}\n{song_artist}\n\n{lyrics}\n\n{auto_hastag(song_title, song_artist)}"
    return formatted_lyrics

# Helper function to generate hashtags
def auto_hastag(title, artist):
    artist = artist.replace(" ", "")
    hasttag = f"Tags: {title.lower()}, {artist.lower()}, songlyrics"
    return hasttag

# Helper function to save lyrics to a CSV file
def auto_save(title, artist):
    filename = "./Song Finder/song_saved.csv"
    
    # Ensure the file exists
    if not os.path.exists(filename):
        try:
            with open(filename, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(["Title", "Artist"])  # Optional: Write headers
            print(f"{filename} created successfully.")
        except Exception as e:
            print(f"Error creating {filename}: {e}")
            return

    # Check for existing title and save if new
    try:
        with open(filename, 'r+', newline='') as file:
            reader = csv.reader(file)
            for row in reader:
                if row[0] == title:
                    print(f"{title} already exists in {filename}.")
                    return
            writer = csv.writer(file)
            writer.writerow([title, artist])
            print(f"{title} by {artist} saved to {filename}.")
    except Exception as e:
        print(f"Error accessing {filename}: {e}")

# Function to search for lyrics and display results
def search_lyrics(event=None):
    global copied
    copied = False  # Reset the copied flag when searching for new lyrics
    song_name = song_entry.get()
    print("Searching for lyrics...")

    def perform_search():
        nonlocal song_name
        if song_name:
            results = genius.search_songs(song_name, per_page=6)
            if results['hits']:
                song_list.delete(0, tk.END)
                for hit in results['hits']:
                    song_list.insert(tk.END, f"{hit['result']['title']} by {hit['result']['primary_artist']['name']}")
                song_list.pack(side=tk.TOP, fill=tk.X)
            else:
                print("No songs found with that title.")

    # Perform the search in a separate thread
    search_thread = threading.Thread(target=perform_search)
    search_thread.start()

# Function to display lyrics when a song is selected
def on_song_select(event):
    selection = event.widget.curselection()
    if selection:
        index = selection[0]
        song_name = event.widget.get(index)
        # Extract the title and artist from the selection
        title, artist = song_name.split(" by ")
        song = genius.search_song(title, artist)
        if song:
            formatted_lyrics = format_lyrics(song)
            lyrics_text.configure(state="normal")
            lyrics_text.delete("1.0", tk.END)
            lyrics_text.insert(tk.END, formatted_lyrics)
            lyrics_text.configure(state="disabled")
            print("Lyrics displayed successfully.")
            auto_copy()
            auto_save(title, artist)

# Function to copy lyrics to clipboard
def auto_copy():
    global copied
    if not copied and lyrics_text.get("1.0", tk.END).strip():
        root.clipboard_clear()
        root.clipboard_append(lyrics_text.get("1.0", tk.END).strip())
        copied = True
        print("Lyrics copied to clipboard.")

# Function to reset the application
def reset_lyrics():
    global copied
    copied = False  # Reset the copied flag
    song_entry.delete(0, tk.END)
    lyrics_text.configure(state="normal")
    lyrics_text.delete("1.0", tk.END)
    lyrics_text.configure(state="disabled")
    song_list.delete(0, tk.END)  # Clear the song list
    print("Application reset. Ready to search again.")

# Function to handle key press events
def on_key_press(event):
    # Check if the 'r' key is pressed and the lyrics_text widget is not empty
    if event.char == 'r' and lyrics_text.get("1.0", tk.END).strip():
        reset_lyrics()

# Create the main window
root = tk.Tk()
root.title("Song Lyrics Search")

# Create the search frame
search_frame = tk.Frame(root)
search_frame.pack(pady=10, padx=10, fill=tk.X)

# Create the song entry field
song_entry = tk.Entry(search_frame, width=100)
song_entry.pack(side=tk.LEFT, padx=(0, 5))
song_entry.bind("<Return>", search_lyrics)

# Create the search button
search_button = tk.Button(search_frame, text="Search", command=search_lyrics)
search_button.pack(side=tk.LEFT)

# Create the song list
song_list = tk.Listbox(root, height=6)
song_list.bind("<<ListboxSelect>>", on_song_select)
song_list.pack(pady=10, fill=tk.X)

# Create the lyrics frame
lyrics_frame = tk.Frame(root)
lyrics_frame.pack(pady=10, fill=tk.BOTH, expand=True)

# Create the lyrics text widget with scrollbar
lyrics_text = scrolledtext.ScrolledText(lyrics_frame, height=20, width=60, state="disabled", font=("Verdana", 10), fg="black")
lyrics_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# Create the reset button
reset_button = tk.Button(root, text="Reset", command=reset_lyrics)
reset_button.pack(pady=10)

# Create the status frame at the bottom
status_frame = tk.Frame(root)
status_frame.pack(fill=tk.X)
status_text = tk.Text(status_frame, height=4, state="disabled", bg="light gray", font=("Verdana", 8))
status_text.pack(fill=tk.X)

# Bind the 'r' key press to the reset function
root.bind('<KeyPress>', on_key_press)

# Redirect print statements to the status_text widget
sys.stdout = Redirect(status_text)

# Set the copied flag
copied = False

# Run the main event loop
root.mainloop()
