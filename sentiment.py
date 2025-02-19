import sqlite3 
from bs4 import BeautifulSoup 
from bs4 import Comment 
import re 
 
# Function to parse the .tff lexicon file and return a sentiment 
dictionary 
def parse_tff_file(tff_file): 
    sentiment_dict = {} 
    try: 
        with open(tff_file, 'r') as file: 
            for line in file: 
                if line.strip():   
                    fields = line.strip().split() 
                    word = None 
                    sentiment_score = 0 
 
                    # parsing fields to get word and sentiment score 
                    for field in fields: 
                        if field.startswith("word1="): 
                            word = field.split("=")[1] 
                        elif field.startswith("priorpolarity="): 
                            polarity = field.split("=")[1] 
                            sentiment_score = -1 if polarity == "negative" 
else 1 
                        elif field.startswith("type="): 
                            word_type = field.split("=")[1] 
                            if word_type == "strongsubj": 
                                sentiment_score *= 2   
 
                    if word: 
                        sentiment_dict[word] = sentiment_score 
    except Exception as e: 
        print(f"Error reading .tff file: {e}") 
 
    return sentiment_dict 
 
# function to extract sentiment from lyrics based on the sentiment 
dictionary 
def analyze_sentiment(lyrics, sentiment_dict): 
    sentiment_score = 0 
    try: 
        words = lyrics.split() 
        for word in words: 
            word = word.lower().strip(",.!?")   
            if word in sentiment_dict: 
                sentiment_score += sentiment_dict[word] 
    except Exception as e: 
        print(f"Error analyzing sentiment: {e}") 
    
    return sentiment_score 
 
# function to update sentiment score in the database for each song 
def update_sentiment_in_database(database_file, sentiment_dict): 
    try: 
        conn = sqlite3.connect(database_file) 
        cursor = conn.cursor() 
 
        cursor.execute("SELECT id, lyrics FROM songs") 
        rows = cursor.fetchall() 
 
        for row in rows: 
            song_id = row[0] 
            lyrics = row[1] 
            sentiment_score = analyze_sentiment(lyrics, sentiment_dict) 
 
            # updating the sentiment score for the song in the database 
            cursor.execute(""" 
                UPDATE songs 
                SET sentiment_score = ? 
                WHERE id = ? 
            """, (sentiment_score, song_id)) 
 
        conn.commit() 
        conn.close() 
        print("Sentiment scores updated successfully!") 
    except Exception as e: 
        print(f"Error updating sentiment in database: {e}") 
 
# function to scrape song data and update database 
def scrape_and_update_data(database_file, tff_file): 
 
    sentiment_dict = parse_tff_file(tff_file) 
    
    update_sentiment_in_database(database_file, sentiment_dict) 
 
# Main script 
if __name__ == "__main__": 
 
    database_file = ('nick_cave_lyrics4.db')   
 
    tff_file = ('subjclueslen1-HLTEMNLP05.tff')   
 
    scrape_and_update_data(database_file, tff_file) 
 
print("Done.")
