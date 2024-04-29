# Song Lyrics Search

A Python application that allows you to search for song lyrics using the Genius API.

## Features

- Search for song lyrics by song title.
- Display a list of search results with song titles and artists.
- View formatted lyrics with song title, artist, and tags.
- Automatically copy lyrics to the clipboard.
- Save the history of the song you get to a CSV file.

## Prerequisites

- Python 3.x
- `tkinter` (usually included with Python)
- `lyricsgenius` library
- Genius API token

### Getting the Genius API Token

1. Go to the [Genius Developer Portal](https://genius.com/developers) and sign up (or sign in if you already have an account).
2. Create a new Client Access Token by clicking on "Create New" under the "Client Access Tokens" section.
3. Copy the token and replace `'YOUR_GENIUS_API_TOKEN_HERE'` in the code with your actual token.

### Installing Dependencies

1. Install the `lyricsgenius` library by running the following command:
   ```bash
   pip install lyricsgenius

## Usage

1. Clone or download the project repository.
2. Open the project in your preferred Python IDE (e.g., PyCharm, Visual Studio Code).
3. Replace `'YOUR_GENIUS_API_TOKEN_HERE'` in the code with your actual Genius API token.
4. Run the `lyrcisfinder.py` file.
5. Enter a song title in the search field and click the "Search" button or press Enter.
6. Select a song from the list of search results.
7. The formatted lyrics will be displayed in the lyrics text area and automatically copied to the clipboard.
8. The lyrics will also be saved to a CSV file in the `./Song Finder/song_saved.csv` directory.

## Main Functions

- `search_lyrics`: Searches for song lyrics based on the user's input.
- `on_song_select`: Displays the formatted lyrics when a song is selected from the search results.
- `auto_copy`: Automatically copies the lyrics to the clipboard.
- `auto_save`: Saves the lyrics to a CSV file.
- `reset_lyrics`: Resets the application and clears the search results and lyrics display.
- `on_key_press`: Handles the 'r' key press event to reset the application.

## Dependencies

- `tkinter`: Python's standard GUI library (usually included with Python).
- `lyricsgenius`: A Python library for accessing song lyrics from Genius.com.
- `re`: Python's regular expression library for text manipulation.
- `threading`: Python's library for creating and managing threads.
- `os`: Python's library for interacting with the operating system.
- `csv`: Python's library for reading and writing CSV files.

## IDE

This project was developed using Python 3.x and can be opened and run in any Python IDE or text editor that supports Python development. Popular choices include PyCharm, Visual Studio Code, and Sublime Text.

## License

This project is licensed under the [MIT License](https://choosealicense.com/licenses/mit/).
