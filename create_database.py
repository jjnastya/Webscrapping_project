import sqlite3 
 
# creating an sqlite database 
conn = sqlite3.connect("nick_cave_lyrics4.db") 
cursor = conn.cursor() 
 
# creating the table 
cursor.execute(""" 
CREATE TABLE IF NOT EXISTS songs ( 
    id INTEGER PRIMARY KEY AUTOINCREMENT, 
    song_name TEXT, 
    album_name TEXT, 
    release_year INTEGER, 
    lyrics TEXT 
) 
""") 
 
conn.commit() 
conn.close() 
 
# checking if everything was created 
 
print("Done.") 
