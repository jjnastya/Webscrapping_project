from bs4 import BeautifulSoup 
from bs4 import Comment 
import sqlite3 
import os 
import re 
 
def get_lyrics(soup): 
    try: 
        # locating the comment where the lyrics start 
        start_comment = soup.find(string=lambda text: isinstance(text, 
Comment) and "Sorry about that" in text) 
        
        if start_comment: 
            # finding the <div> containing the comment 
            div_containing_comment = start_comment.find_parent('div') 
            
            # extracting the text from this <div> 
            if div_containing_comment: 
                lyrics = div_containing_comment.get_text(strip=True, 
separator='\n') 
                return lyrics 
        
        return "Lyrics not found" 
    
    except Exception as e: 
        print(f"Error extracting lyrics: {e}") 
        return "Error extracting lyrics" 
 
def get_song_name(soup): 
    try: 
        # extracting the script tag containing the song name 
        script_tag = soup.find('script', string=re.compile('SongName')) 
        
        if script_tag: 
            # searching for the SongName value within the script tag using 
regex 
            match = re.search(r'SongName\s*=\s*"([^"]+)"', 
script_tag.string) 
            
            if match: 
                song_name = match.group(1)  # getting the value of 
SongName 
                return song_name 
        
        return "Song name not found" 
    
    except Exception as e: 
        print(f"Error extracting song name: {e}") 
        return "Error extracting song name" 
    
 
def get_album_name_and_year(soup): 
    try: 
        # extracting the album name and release year from the page 
        album_info_tag = soup.find('div', class_='songinalbum_title')   
        if album_info_tag: 
            # extracting the album text 
            album_text = album_info_tag.get_text(strip=True) 
            
            # extracting the album name (anything after the first colon 
and before the year) 
            album_name_match = re.search(r'^[^:]+:\s*"([^"]+)"', 
album_text) 
            if album_name_match: 
                album_name = album_name_match.group(1)   
            else: 
                album_name = "Album not found" 
            
            # extracting the release year 
            year_match = re.search(r'\((\d{4})\)', album_text) 
            if year_match: 
                release_year = year_match.group(1)   
            else: 
                release_year = "Year not found" 
            
            return album_name, release_year 
        return "Album not found", "Year not found" 
    except Exception as e: 
        print(f"Error extracting album name and year: {e}") 
        return "Album not found", "Year not found" 
 
# defying a function to scrape albums and songs from all HTML files in the 
folder 
def scrape_albums_and_songs_in_files(folder_path): 
    # looping through all HTML files in the folder 
    for filename in os.listdir(folder_path): 
        if filename.endswith(".html"): 
            file_path = os.path.join(folder_path, filename) 
            print(f"Processing file: {file_path}") 
            
            with open(file_path, "r", encoding="utf-8") as file: 
                soup = BeautifulSoup(file, 'html.parser') 
 
                # extracting song details 
                song_name = get_song_name(soup) 
                album_name, release_year = get_album_name_and_year(soup) 
                lyrics = get_lyrics(soup) 
                
                # inserting the data into the database 
                cursor.execute(""" 
                    INSERT INTO songs (song_name, album_name, 
release_year, lyrics) 
                    VALUES (?, ?, ?, ?) 
                """, (song_name, album_name, release_year, lyrics)) 
 
                conn.commit() 
 
# connect to my existing sqlite database 
conn = sqlite3.connect('nick_cave_lyrics4.db')   
cursor = conn.cursor() 
 
html_folder_path = "htmls"   
 
# the scraping function 
scrape_albums_and_songs_in_files(html_folder_path) 
 
conn.close() 
 
print("Scraping and database insertion completed") 
