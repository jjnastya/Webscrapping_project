import sqlite3 
import pandas as pd 
 
def export_data_to_excel(database_file, output_excel): 
    try: 
        conn = sqlite3.connect("nick_cave_lyrics4.db") 
        query = "SELECT song_name, album_name, release_year, lyrics, 
sentiment_score FROM songs" 
        
        df = pd.read_sql(query, conn) 
 
        df.to_excel(output_excel, index=False) 
        
        print(f"Data successfully exported to {output_excel}") 
    except Exception as e: 
        print(f"Error exporting data: {e}") 
    finally: 
        conn.close() 
 
export_data_to_excel("nick_cave_lyrics4.db", 
"sentiment_analysis_results3.xlsx")
